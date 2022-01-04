from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from blog_app.models import *


# ---------------------------------------------------------------------------- #
#                                PostCreateForm                                #
# ---------------------------------------------------------------------------- #


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        exclude = ('author', 'status' )
        # fields = '__all__'
        
    # def __init__(self, *args, **kwargs):
    #     super(PostCreateForm, self).__init__(*args, **kwargs)
        
    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class': 'input'})
    


# ---------------------------------------------------------------------------- #
#                                  CommentForm                                 #
# ---------------------------------------------------------------------------- #


class CommentForm(ModelForm):
    
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body', )
        