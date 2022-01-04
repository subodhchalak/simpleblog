from django.forms.models import construct_instance
from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls.base import reverse

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from blog_app.models import *
from blog_app.forms import *

from django.contrib import messages

from django.db.models import Q



# Create your views here.



# ---------------------------------------------------------------------------- #
#                                  index View                                  #
# ---------------------------------------------------------------------------- #

def index(request):
    all_posts = Post.objects.all()
    all_tags = Tag.objects.all()
    template_name = 'blog_app/index.html'
    context={'all_posts': all_posts, 'all_tags':all_tags}
    return render(request, template_name, context)

# ---------------------------------------------------------------------------- #
#                                 TagCreateView                                #
# ---------------------------------------------------------------------------- #

class TagCreateView(CreateView):
    model = Tag
    fields = '__all__'
    template_name = 'blog_app/tag_form.html'
    success_url = reverse_lazy('tag-list')


# ---------------------------------------------------------------------------- #
#                                 TagList View                                 #
# ---------------------------------------------------------------------------- #

class TagListView(generic.ListView):
    model = Tag
    template_name = 'blog_app/tag_list.html'
  
    
# ---------------------------------------------------------------------------- #
#                                 TagDetailView                                #
# ---------------------------------------------------------------------------- #


class TagDetailView(generic.DetailView):
    model = Tag
    template_name = 'blog_app/tag_detail.html'


# ---------------------------------------------------------------------------- #
#                                 PostListView                                 #
# ---------------------------------------------------------------------------- #

class PostListView(generic.ListView):
    model = Post
    all_tags = Tag.objects.all()
    extra_context= {'all_tags': all_tags}
    template_name = 'blog_app/post_list.html'
    pagiante_by = 1
    
    
# # ---------------------------------------------------------------------------- #
# #                                PostDetailView                                #
# # ---------------------------------------------------------------------------- #




def post_detail(request, pk):
    
    post_instance = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post= post_instance, status=True)
    
    form = CommentForm()
    
    new_comment = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post_instance
            new_comment.save()

            messages.success(request, 'Your comment was successfully submitted!')
            return redirect("post-detail", post_instance.id)
    
    template_name = 'blog_app/post_detail.html'
    context = {
        'post_instance': post_instance,
        'form' : form,
        'comments' : comments,
        'new_comment' : new_comment,
    }
    
    return render(request, template_name, context)
        








# class PostDetailView(generic.DetailView):
#     model = Post
#     all_tags = Tag.objects.all()
#     extra_context = {'all_tags':all_tags}
#     template_name = 'blog_app/post_detail.html'



# def post_detail(request, pk):
    
#     try:
#         post_instance = Post.objects.get(pk=pk)                      # get the post
#         comments = Comment.objects.filter(post=post_instance)        # try filtering all the comments of post
#         profile_instance = request.user.profile                       # instance of user profile
#         comment_instance = Comment.objects.filter(commenter=profile_instance) # try filtering all the comments of
#     except Post.DoesNotExist:
#         raise Http404('Data does not exist')
    
    
#     all_tags = Tag.objects.all()                                      # getting all tags 
#     profile_list = Profile.objects.filter()
    
#     form = CommentForm()
    
#     new_comment = None
    
#     if request.method == 'POST':
#         form = CommentForm(data=request.POST)
        
#         if form.is_valid():
#             new_comment = form.save(commit=False)
#             new_comment.commenter = request.user.profile
#             new_comment.post = post_instance
#             new_comment.save()
            
#             messages.success(request, "Comment added successfully!")
#             return redirect("/")

#     template_name = 'blog_app/post_detail.html'
#     context = {
#         'post_instance': post_instance,
#         'all_tags': all_tags,
#         'form' : form,
#         'comments' : comments,
#         'profile_instance' : profile_instance,
#         'profile_list': profile_list,
#         'comment_instance' : comment_instance,
#         'new_comment' : new_comment,
#     }
    
#     return render(request, template_name, context)


# ---------------------------------------------------------------------------- #
#                               post_create View                               #
# ---------------------------------------------------------------------------- #


@login_required(login_url='login')
def post_create(request):
    try:
        profile_instance = request.user.profile
    except:
        return redirect('user-account-edit')
    
    profile_instance = request.user.profile
    form = PostCreateForm()
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = profile_instance
            post.save()
            form.save_m2m()
            messages.success(request, 'Post addess successfully')
            return redirect('user-account')

    template_name = 'blog_app/post_form.html'
    context = {'form': form, 'profile_instance':profile_instance}
    return render(request, template_name, context)


# ---------------------------------------------------------------------------- #
#                               post_update View                               #
# ---------------------------------------------------------------------------- #


@login_required(login_url="login")
def post_update(request, pk):
    post_instance = Post.objects.get(pk=pk)
    profile_instance = request.user.profile
    
    form = PostCreateForm(instance=post_instance)
    
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=post_instance, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully")
            return redirect('user-account')
        
    template_name = 'blog_app/post_form.html'
    context = {
        'post_instance': post_instance,
        'profile_instance' : profile_instance,
        'form': form,
    }
    
    return render(request, template_name, context)


# ---------------------------------------------------------------------------- #
#                                PostDelete View                               #
# ---------------------------------------------------------------------------- #


@login_required(login_url='login')
def post_delete(request, pk):
    
    profile_instance = request.user.profile
    post_instance = get_object_or_404(Post, pk=pk)
    
    if request.method=='POST':
        post_instance.delete()
        messages.success(request, "Post deleted successfully")
        return redirect('user-account')
    
    template_name = 'blog_app/post_confirm_delete.html'
    context = {'post_instance': post_instance, 'profile_instance':profile_instance}
    return render(request, template_name, context)


# ---------------------------------------------------------------------------- #
#                                comment_delete View                           #
# ---------------------------------------------------------------------------- #


# @login_required(login_url='login')
# def comment_delete(request, pk):
    
#     profile_instance = request.user.profile
#     comment_instance = get_object_or_404(Comment, pk=pk)
    
#     if request.method == 'POST':
#         comment_instance.delete()
#         messages.success(request, 'Comment deleted successfully')
#         return redirect('user-account')
    
#     template_name = 'blog_app/comment_confirm_delete.html'
#     context = {'profile_instance': profile_instance, 'comment_instance': comment_instance}
#     return render(request, template_name, context)
    
    
# ---------------------------------------------------------------------------- #
#                                search_results                                #
# ---------------------------------------------------------------------------- #
    
    
def search_results(request):
   
    if request.method == 'POST':
        query = request.POST.get('query')           # 'query' denotes the  search query name metioned in search box form in navabar.html

        if query != '':                             # check if query is not a empty string
            search_objects = Post.objects.filter(
                Q(title__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__last_name__icontains=query) |
                Q(tags__name__icontains=query)    
            ).distinct()
        
            context = {'query': query, 'search_objects': search_objects}
            template_name= 'search_results.html' 
            return render(request, template_name, context)
        else:
            return redirect("/")
        
        
        
def error_404(request, exception):
    return render(request, 'error_404.html')

