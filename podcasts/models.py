from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import uuid

def podcast_path(instance, filename):
    return '{0}/{1}'.format(instance.slug, filename)

def item_path(instance, filename):
    return '{0}/{1}'.format(instance.podcast.slug, filename)

class Podcast(models.Model):
    owner = models.ForeignKey(User, related_name='podcasts', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_build_date = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    slug = models.SlugField(unique=True)
    subtitle = models.TextField(blank=True)
    itunes_type = models.TextField(blank=True)
    author = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    image = models.ImageField(upload_to=podcast_path, blank=True)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=2, blank=True)
    copyright = models.TextField(blank=True)
    block = models.BooleanField(default=False)
    explicit = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            podcast_slug = slugify(self.title)
            self.slug = podcast_slug
        super(Podcast, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Item(models.Model):
    podcast = models.ForeignKey(Podcast, related_name='items', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.TextField()
    slug = models.SlugField(unique=True)
    episode_type = models.TextField(blank=True)
    order = models.IntegerField(blank=True, null=True)
    season = models.IntegerField(blank=True, null=True)
    episode = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    copyright = models.TextField(blank=True)
    guid = models.UUIDField(default=uuid.uuid4, editable=False)
    author = models.TextField(blank=True)
    enclosure = models.FileField(upload_to=item_path)
    media_type = models.TextField(blank=True)
    duration = models.IntegerField(default=0)
    file_size = models.IntegerField()
    image = models.ImageField(upload_to=item_path, blank=True)
    block = models.BooleanField(default=False)
    explicit = models.BooleanField(default=False)
    closed_captioned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            item_slug = slugify(self.title)
            self.slug = item_slug
            self.file_size = self.enclosure.size
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Category(models.Model):
    podcast = models.ForeignKey(Podcast, related_name='categories', on_delete=models.CASCADE)
    name = models.TextField()
    slug = models.SlugField()
    parent_name = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
