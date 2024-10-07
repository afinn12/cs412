
## formdata/urls.py
## define the URLs for this app

from django.urls import path
from .views import ShowAllView # our view class definition 

# define a list of valid URL patterns:
urlpatterns = [
    # map the URL (empty string) to the view
    path('', ShowAllView.as_view(), name='show_all'), # generic class-based view
]
