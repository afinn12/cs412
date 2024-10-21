## Create View
# mini_fb/views.py
# Define the views for the mini_fb app:
#from django.shortcuts import render
from .models import Profile, Image
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from typing import Any
from .forms import * ## import the forms (e.g., CreateStatusMessageForm)
from django.views.generic.edit import UpdateView ## add UpdateView to list of imports
from .forms import UpdateProfileForm

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
    template_name = "mini_fb/create_status_form.html"

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
        # find the Profile identified by the PK from the URL pattern
        return reverse('profile', kwargs={'pk':self.kwargs['pk']})

    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''

        # find the Profile identified by the PK from the URL pattern
        profile = Profile.objects.get(pk=self.kwargs['pk'])

        # attach this Profile to the instance of the StatusMessage to set its FK
        form.instance.profile = profile # like: StatusMessage.profile = profile

        # save the status message to database
        sm = form.save()
        
        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image.objects.create(status=sm, image_file=file)
            image.save()  

        # delegate work to superclass version of this method
        return super().form_valid(form)    

    
class CreateProfileView(CreateView):
    '''
    A view to create a StatusMessage on a Profile.
    on GET: send back the form to display
    on POST: read/process the form, and save new StatusMessage to the database
    '''

    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # get the context data from the superclass
        context =  super().get_context_data(**kwargs)
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # find the Profile identified by the PK from the URL pattern
        return reverse('profile', kwargs={'pk': self.object.pk})


    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''
        # delegate work to superclass version of this method
        return super().form_valid(form)
    

class UpdateProfileView(UpdateView):
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile