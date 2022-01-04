from django.urls import path

from user_app.views import *

urlpatterns = [
    path('registration/', registration, name='registration'),
    
    path('user_account/', user_account, name='user-account'),
    path('user_account_edit/', user_account_edit, name='user-account-edit'),
    
    path('user_username_edit/', user_username_edit, name='user-username-edit'),
    path('user_confirm_delete/', user_delete, name='user-confirm-delete'),
    
    
    path('user_profiles/', UserProfileListView.as_view(), name='user-profiles'),
    path('user_profiles/<int:pk>/detail/', UserProfileDetailView.as_view(), name='user-profiles-detail')
]
