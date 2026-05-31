from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    image_data=models.BinaryField(null=True, blank=True)
    image_mime_type = models.CharField(max_length=50, null=True, blank=True)
    created_at=models.DateField(auto_now_add=True)
    slug=models.SlugField(unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    is_piublished=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug= slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def formatted_img_url(self):
        if self.image.__str__().startswith(('http://','https://')):
            url=self.image
        else:
            url=self.image.url
        return url

    def __str__(self):
        return self.title


class AboutUs(models.Model):
    content=models.TextField()
    