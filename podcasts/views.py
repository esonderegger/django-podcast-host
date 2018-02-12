from podcasts.models import Podcast, Item, Category
from podcasts.serializers import PodcastSerializer, ItemSerializer, CategorySerializer
from rest_framework import generics, permissions
from django.shortcuts import render

def all_data(request):
    podcasts = Podcast.objects.all()
    if request.is_secure():
        root_url = 'https://'
    else:
        root_url = 'http://'
    root_url += request.get_host() + '/'
    the_dict = {
        'podcasts': podcasts,
        'root_url': root_url,
    }
    return the_dict


def podcast_data(request, slug):
    the_podcast = Podcast.objects.get(slug=slug)
    the_categories = Category.objects.filter(podcast_id=the_podcast.id)
    the_items = Item.objects.filter(podcast_id=the_podcast.id)
    if request.is_secure():
        root_url = 'https://'
    else:
        root_url = 'http://'
    root_url += request.get_host() + '/'
    the_dict = {
        'podcast': the_podcast,
        'categories': the_categories,
        'items': the_items,
        'root_url': root_url,
    }
    return the_dict


def item_data(request, slug, item_slug):
    the_podcast = Podcast.objects.get(slug=slug)
    the_item = Item.objects.get(podcast_id=the_podcast.id, slug=item_slug)
    if request.is_secure():
        root_url = 'https://'
    else:
        root_url = 'http://'
    root_url += request.get_host() + '/'
    the_dict = {
        'podcast': the_podcast,
        'item': the_item,
        'root_url': root_url,
    }
    return the_dict


def xmlfeed(request, slug):
    return render(request, 'podcasts/feed.xml', podcast_data(request, slug))


def listpage(request):
    return render(request, 'podcasts/all.html', all_data(request))


def htmlpage(request, slug):
    return render(request, 'podcasts/feed.html', podcast_data(request, slug))


def itempage(request, slug, item_slug):
    return render(request, 'podcasts/item.html', item_data(request, slug, item_slug))


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj, request.user)
        if type(obj) is Podcast:
            return obj.owner == request.user
        return obj.podcast.owner == request.user


class PodcastList(generics.ListCreateAPIView):
    permission_classes = (IsOwner,)
    queryset = Podcast.objects.all()
    serializer_class = PodcastSerializer

    def get_queryset(self):
        if self.request.user.id:
            return Podcast.objects.filter(owner=self.request.user)
        return []

    def perform_create(self, serializer):
        if (self.request.user.id):
            serializer.save(owner=self.request.user)


class PodcastDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = PodcastSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Podcast.objects.filter(slug=self.kwargs['slug'])


class ItemList(generics.ListCreateAPIView):
    permission_classes = (IsOwner,)
    serializer_class = ItemSerializer

    def get_queryset(self):
        the_podcast = Podcast.objects.get(slug=self.kwargs['slug'])
        print(the_podcast)
        return Item.objects.filter(podcast_id=the_podcast.id)

    def perform_create(self, serializer):
        the_podcast = Podcast.objects.get(slug=self.kwargs['slug'])
        print(the_podcast)
        serializer.save(podcast_id=the_podcast.id)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = ItemSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Item.objects.filter(slug=self.kwargs['slug'])


class CategoryList(generics.ListCreateAPIView):
    permission_classes = (IsOwner,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        the_podcast = Podcast.objects.get(slug=self.kwargs['slug'])
        return Category.objects.filter(podcast_id=the_podcast.id)

    def perform_create(self, serializer):
        the_podcast = Podcast.objects.get(slug=self.kwargs['slug'])
        serializer.save(podcast_id=the_podcast.id)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.filter(slug=self.kwargs['slug'])
