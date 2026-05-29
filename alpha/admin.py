from django.contrib import admin
from django import forms
from .models import Post, Category, AboutUs


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')


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