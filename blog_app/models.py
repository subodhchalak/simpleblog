from django.db import models

from django.contrib.auth.models import User
import uuid

from user_app.models import *

# Create your models here.


# ---------------------------------------------------------------------------- #
#                                   Tag Model                                  #
# ---------------------------------------------------------------------------- #


class Tag(models.Model):
    
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('-created', )


# ---------------------------------------------------------------------------- #
#                                  Post Model                                  #
# ---------------------------------------------------------------------------- #


class Post(models.Model):
    
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag)
    
    title = models.CharField(max_length=300)
    body = models.TextField(max_length=5000)
    post_image = models.ImageField(upload_to='posts/', default="posts/simpleblog.jpg", blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    
    status = models.BooleanField(default=True, null=True)
    
    def __str__(self):
        return (f"{self.title} - {self.author}")
    
    class Meta:
        ordering = ('-created', )
        

    
    
# ---------------------------------------------------------------------------- #
#                                 Review Model                                 #
# ---------------------------------------------------------------------------- #


class Comment(models.Model):
    
    # commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    name= models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=200, null=True,)
    body = models.TextField(max_length=500, help_text="Put your brief comment in 500 characters")

    created = models.DateTimeField(auto_now_add=True)
    # id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    
    status = models.IntegerField(default=True, null=True)
    
    class Meta:
        ordering = ('created', )
        # unique_together = (('commenter', 'post'), )
    
    def __str__(self):
        return (f"{self.name} - {self.body}")