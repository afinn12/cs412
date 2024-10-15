
## formdata/urls.py
## define the URLs for this app

from django.urls import path
from .views import ShowAllProfiles, ProfileView # our view class definition 

# define a list of valid URL patterns:
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllProfiles.as_view(), name='show_all_profiles'), # generic class-based view
    
    # path(r'', views.RandomArticleView.as_view(), name="random"),    
    # path(r'show_all', views.ShowAllView.as_view(), name="show_all"), 
    path(r'profile/<int:pk>', ProfileView.as_view(), name="profile"), 
    # path(r'create_comment', views.CreateCommentView.as_view(), name="create_comment"), 
    # path(r'article/<int:pk>/create_comment', views.CreateCommentView.as_view(), name="create_comment"), ## NEW 
]
