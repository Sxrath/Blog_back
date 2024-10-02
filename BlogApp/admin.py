from django.contrib import admin

from .models import BlogPost,Profile,Tag

# Register your models here.
admin.site.register(BlogPost),
admin.site.register(Profile),
admin.site.register(Tag)