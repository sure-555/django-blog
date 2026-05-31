from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.CharField(max_length=500, null=True, blank=True)
    image_data = models.BinaryField(null=True, blank=True) 
    image_mime_type = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, unique=True)
    is_piublished = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    # ---> PASTE IT EXACTLY HERE, INSIDE THE MODEL CLASS <---
    @property
    def image_base64(self):
        if self.image_data and self.image_mime_type:
            binary_as_string = base64.b64encode(self.image_data).decode('utf-8')
            return f"data:{self.image_mime_type};base64,{binary_as_string}"
        elif self.image:
            return self.image
        return None 


class AboutUs(models.Model):
    content=models.TextField()
    