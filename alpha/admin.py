from django.contrib import admin
from .models import Post,Category,AboutUs

class PostAdmin(admin.ModelAdmin):
    list_display=('title','content')
    search_fields=('title','content')


# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(AboutUs)
