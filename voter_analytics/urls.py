## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from .views import *

urlpatterns = [
    path('', VoterListView.as_view(), name="voter_home"),
    path('results', VoterListView.as_view(), name="voter_results"),
]
