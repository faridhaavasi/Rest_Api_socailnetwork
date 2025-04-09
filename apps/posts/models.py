from django.db import models
from django.contrib.auth import get_user_model # Import the custom user model
from django.utils import timezone
from django.utils.text import slugify



user = get_user_model() # Custom user model global variable

class PostManager(models.Manager):
    def posts_published(self):
        return self.filter(is_published=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(user, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    objects = PostManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def publish(self):
        self.is_published = True
        self.published_at = timezone.datetime.now()
        self.save()

    def __str__(self):
        return f'{self.title} by {self.author.email}'