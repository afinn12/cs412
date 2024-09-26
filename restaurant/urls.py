
## formdata/urls.py
## define the URLs for this app

from django.urls import path
from django.conf import settings
from . import views

# define a list of valid URL patterns:
urlpatterns = [
    path(r'', views.show_main, name="show_main"), 
    path(r'main', views.show_main, name="show_main"), 
    path(r'order', views.show_order, name="show_order"), 
    path(r'confirmation', views.show_confirmation, name="show_confirmation"), 
]
