from rest_framework import serializers
from podcasts.models import Podcast, Item, Category


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        exclude = ('id', 'podcast')
        read_only_fields = (
            'slug',
            'pub_date',
            'guid',
            # 'duration', todo: use ffprobe to detect duration
            # 'media_type', todo: use ffprobe to detect media_type
            'file_size',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id', 'podcast')
        read_only_fields = ('slug',)


class PodcastSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Podcast
        exclude = ('id', 'owner', 'created')
        read_only_fields = ('slug', 'last_build_date')
