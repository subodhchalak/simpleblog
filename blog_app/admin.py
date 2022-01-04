from django.contrib import admin

from blog_app.models import *

# Register your models here.


# ------------------------------------- X ------------------------------------ #

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


# ------------------------------------- X ------------------------------------ #


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author']
    list_filter = ['id', 'title', 'author', 'tags']
    inlines = [CommentInline]
    
    
# ------------------------------------- X ------------------------------------ #


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',  'created']
    list_filter = ['id', 'name',  'created']
   
   
# ------------------------------------- X ------------------------------------ # 
  
    
@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ['post', 'name', 'created', 'status']
    list_filter = ['created', 'status']
    search_fields = ['post', 'name', 'body']
    
# ------------------------------------- X ------------------------------------ #