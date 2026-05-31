from django.contrib import admin
from django import forms
from .models import Post, Category, AboutUs

class PostAdmin(admin.ModelAdmin):
    # Added category and created_at columns for better visibility in the admin list view
    list_display = ('title', 'category', 'created_at')
    search_fields = ('title', 'content')
    
    # This magic line automatically builds the slug in real-time as you type the title!
    prepopulated_fields = {'slug': ('title',)}


class AboutUsAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 15,
            'cols': 100
        })
    )

    class Meta:
        model = AboutUs
        fields = '__all__'


class AboutUsAdmin(admin.ModelAdmin):
    form = AboutUsAdminForm


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(AboutUs, AboutUsAdmin)