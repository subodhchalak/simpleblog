from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.contrib import messages

from user_app.forms import CustomUserCreationForm

from django.contrib.auth import login, logout, authenticate

from user_app.models import *
from user_app.forms import *

from blog_app.models import *


from django.contrib.auth.decorators import login_required


from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

# Create your views here.


# ---------------------------------------------------------------------------- #
#                               registration View                              #
# ---------------------------------------------------------------------------- #


def registration(request):
    user = request.user
    
    if user.is_authenticated:
        return redirect('index')
    
    else:
        
        form = CustomUserCreationForm()
        
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save(commit=False)
                user.username=user.username.lower()
                form.save()
                message = "Registration Successful"
                messages.success(request, message)
                return redirect('login')
            else:
                messages.error(request, "Registration Failure")
            
        context = {'form': form, }
        template_name = 'registration/register_user.html'
        
        return render(request, template_name, context)
    
    
    
# ---------------------------------------------------------------------------- #
#                                 user_account view                                 #
# ---------------------------------------------------------------------------- #

@login_required(login_url='login')
def user_account(request):
    profile_instance = Profile.objects.get_or_create(user=request.user)
    # post_count = profile_instance.objects.filter('post').count()
    context = {'profile_instance':profile_instance[0],}        # get_or_create return a tuple, so take first value
    template_name = 'user_app/user_account.html'
    return render(request, template_name, context)


# ---------------------------------------------------------------------------- #
#                            user_account_edit View                            #
# ---------------------------------------------------------------------------- #


@login_required(login_url='login')
def user_account_edit(request):
    profile_instance = Profile.objects.get_or_create(user=request.user)
    form = ProfileForm(instance=profile_instance[0])
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile_instance[0], files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('user-account')
        
    context = {'form':form}
    template_name = 'user_app/user_form.html'
    return render(request, template_name, context)



# ---------------------------------------------------------------------------- #
#                              UserProfileListView                             #
# ---------------------------------------------------------------------------- #

class UserProfileListView(generic.ListView):
    model = Profile
    template_name = 'user_app/user_profile_list.html'
    paginate_by = 10
    

# ---------------------------------------------------------------------------- #
#                             UserProfileDetailView                            #
# ---------------------------------------------------------------------------- #

class UserProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'user_app/user_profile_detail.html'
  
  
  
# ---------------------------------------------------------------------------- #
#                              user_username_edit                              #
# ---------------------------------------------------------------------------- #


@login_required(login_url='login')
def user_username_edit(request):
    user= request.user
    form = UserForm()
    if request.method=='POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user.username = user.username.lower()
            form.save()
            messages.success(request, "Username changed successfully!")
            return redirect ('user-account')
    
    context = {'form': form}
    template_name = 'registration/user_username_form.html'
    return render(request, template_name, context)


# ---------------------------------------------------------------------------- #
#                                  user_delete                                 #
# ---------------------------------------------------------------------------- #


def user_delete(request):
    user = request.user
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully')
        return redirect('index')
    
    context = {'user': user}
    template_name = 'registration/user_confirm_delete.html'
    return render(request, template_name, context)