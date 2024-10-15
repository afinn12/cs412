## Create View
# mini_fb/views.py
# Define the views for the mini_fb app:
#from django.shortcuts import render
from .models import Profile
from .forms import * ## import the forms (e.g., CreateStatusMessageForm)
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from typing import Any


# Create your views here.

class ShowAllProfiles(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file


class ProfileView(DetailView):
    '''Display one Profile selected by PK'''
    model = Profile # the model to display
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"


class CreateStatusMessageView(CreateView):
    '''
    A view to create a StatusMessage on a Profile.
    on GET: send back the form to display
    on POST: read/process the form, and save new StatusMessage to the database
    '''

    form_class = CreateStatusMessageForm
    template_name = "blog/create_statusmessage_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # get the context data from the sueprclass
        context =  super().get_context_data(**kwargs)
        # find the Profile identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # add the Profile referred to by the URL into this context
        context['profile'] = profile
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # return 'show_all' # a valid URL pattern
        # return reverse('show_all') # look up the URL called "show_all"

        # find the Profile identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs={'pk':profile.pk})
        # return reverse('profile', kwargs=self.kwargs)

    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''

        # print(f'CreateStatusMessageView.form_valid(): form={form.cleaned_data}')
        # print(f'CreateStatusMessageView.form_valid(): self.kwargs={self.kwargs}')
        # find the Profile identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # attach this Profile to the instance of the StatusMessage to set its FK
        form.instance.profile = profile # like: StatusMessage.profile = profile

        # delegate work to superclass version of this method
        return super().form_valid(form)