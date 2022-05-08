from django.contrib import admin

from app_blog.models import Post,Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
