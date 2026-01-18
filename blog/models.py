from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager  # <--- Added this import

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PUBLISHED)
    read_time = models.PositiveIntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # CHANGED: Used TaggableManager instead of ManyToManyField to 'Tag'
    tags = TaggableManager()
    
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    bookmarks = models.ManyToManyField(User, related_name='bookmarked_posts', blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:110] or 'post'
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        
        # Calculate read time
        words = len(self.content.split())
        self.read_time = max(1, round(words / 200))
        
        super().save(*args, **kwargs)

# DELETED: The 'class Tag' model is gone because django-taggit creates its own tables.

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
