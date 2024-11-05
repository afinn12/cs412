
## formdata/urls.py
## define the URLs for this app

from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ShowAllProfiles, ProfileView, CreateProfileView, CreateStatusMessageView, UpdateProfileView, DeleteStatusMessageView, UpdateStatusView, CreateFriendView, ShowFriendSuggestionsView, ShowNewsFeedView # our view class definition 

# define a list of valid URL patterns:
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfiles.as_view(), name='show_all_profiles'), # generic class-based view
    
    # path(r'', views.RandomArticleView.as_view(), name="random"),    
    # path(r'show_all', views.ShowAllView.as_view(), name="show_all"), 
    path(r'profile/<int:pk>', ProfileView.as_view(), name="profile"), 
    # path(r'create_comment', views.CreateCommentView.as_view(), name="create_comment"), 
    path(r'create_profile', CreateProfileView.as_view(), name="create_profile"), 
    path(r'profile/create_status', CreateStatusMessageView.as_view(), name="create_status"), 
    path(r'profile/update', UpdateProfileView.as_view(), name="update_profile"),
    path(r'status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path(r'status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete_status'),
    path(r'status/<int:pk>/update', UpdateStatusView.as_view(), name='update_status'),
    path('profile/add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), 
]

