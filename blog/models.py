from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_by_category', args=[self.slug])


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
            .filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Our custom manager.
    subtitle = models.CharField(max_length=250)
    body_preview = models.CharField(max_length=250)
    category = models.ForeignKey(Category, related_name='blog_posts')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])


class PostImage(models.Model):
    post_slug = models.CharField(max_length=250)
    image = models.FileField()
    title = models.CharField(max_length=250)

    class Meta:
        db_table = 'image'


class FavPosts(models.Model):
    user = models.ForeignKey(User, related_name='posts_favourite')
    post = models.ForeignKey(Post, related_name='posts_favourite')

    class Meta:
        db_table = 'posts_favourite'


