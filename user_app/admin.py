from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin

from user_app.models import *
from blog_app.models import *
from django.contrib.auth.models import User

# Register your models here.



# class PostInline(admin.TabularInline):
#     model = Post
#     extra = 0


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name']
    list_filter = ['created', ]
    # inlines = [Profile, ]
