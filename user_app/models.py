from django.db import models

from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    first_name = models.CharField(max_length=50,)
    last_name = models.CharField(max_length=50,)
    email = models.EmailField(max_length=200,)
    location = models.CharField(max_length=50,)
    
    bio= models.TextField(max_length=200)
    
    profile_image = models.ImageField(upload_to='profiles/', default='profiles/nopic.png',)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return (f"{self.first_name} {self.last_name}")
    
    class Meta:
        ordering = ('-created', )
        
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
            
        