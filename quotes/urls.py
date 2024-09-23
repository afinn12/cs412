## quotes/urls.py
## description: URL patterns for the quotes app

from django.urls import path
from django.conf import settings
from . import views

# all of the URLs that are part of this app
urlpatterns = [
    path(r'', views.main, name="main"),
    path(r'quote', views.quote, name="quote"),
    path(r'showall', views.showall, name="showall"),
    path(r'about', views.about, name="aboutus"),    
]