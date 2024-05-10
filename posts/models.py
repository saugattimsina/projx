from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


# Create your models here.
class Post(models.Model):
    class Category(models.TextChoices):
        BLOG = (
            "BLOG",
            "Blog",
        )
        NEWS = "NEWS", "News"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, blank=True)
    content = RichTextField()
    image = models.ImageField(upload_to="post/image", null=True, blank=True)
    category = models.CharField(
        max_length=10, choices=Category.choices, default=Category.BLOG
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
