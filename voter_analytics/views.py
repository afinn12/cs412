# blog/views.py
# define the views for the blog app
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Voter


# Create your views here.
class VoterListView(ListView):
    '''View to show a list of voters.'''
    template_name = 'voter_analytics/results.html'  # Update template path
    model = Voter
    context_object_name = 'results'
    paginate_by = 50  # show 50 voter records per page

