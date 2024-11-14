## blog/urls.py
## description: URL patterns for the blog app

from django.urls import path
from .views import *

urlpatterns = [
    path('', VoterListView.as_view(), name="voter_home"),
    path('voters', VoterListView.as_view(), name="voters"),
    path('voter/<str:pk>/', VoterDetailView.as_view(), name='voter_details'),
    path('graphs/', GraphsView.as_view(), name='graphs'),
]
