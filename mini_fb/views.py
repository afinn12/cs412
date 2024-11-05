## Create View
# mini_fb/views.py
# Define the views for the mini_fb app:
#from django.shortcuts import render
from .models import Profile, Image
from django.views.generic import View, ListView, DetailView, CreateView
from django.urls import reverse
from django.shortcuts import redirect
from typing import Any
from .forms import * ## import the forms (e.g., CreateStatusMessageForm)
from django.views.generic.edit import UpdateView ## add UpdateView to list of imports
from .forms import UpdateProfileForm, UpdateStatusForm
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

class ShowAllProfiles(ListView):
    '''Create a subclass of ListView to display all profiles.'''
    model = Profile # retrieve objects of type Profile from the database
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # how to find the data in the template file

    def dispatch(self, request):
        '''add this method to show/debug logged in user'''
        print(f"Logged in user: request.user={request.user}")
        print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        return super().dispatch(request)


class ProfileView(DetailView):
    '''Display one Profile selected by PK'''
    model = Profile # the model to display
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
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
        profile = Profile.objects.get(user=self.request.user)
        # profile = Profile.objects.get(pk=self.kwargs['pk'])
        # add the Profile referred to by the URL into this context
        context['profile'] = profile
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # find the Profile identified by the PK from the URL pattern
        return reverse('profile', kwargs={'pk':self.object.profile.pk})

    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''

        # find the Profile identified by the PK from the URL pattern
        # profile = Profile.objects.get(pk=self.kwargs['pk'])
        profile = Profile.objects.get(user=self.request.user)


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
     
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
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
        context['user_form'] = UserCreationForm()
        return context

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 


    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # find the Profile identified by the PK from the URL pattern
        return reverse('profile', kwargs={'pk': self.object.pk})


    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''
        # Reconstruct the UserCreationForm from the request data
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid() and form.is_valid():  # Validate both forms
            # Save the new user and attach to the profile
            user_instance = user_form.save()
            form.instance.user = user_instance  # Attach the user to the profile
            # Log in the user
            login(self.request, user_instance)

            # Proceed with saving the profile
            return super().form_valid(form)

        # If either form is invalid, re-render the forms with error messages
        return self.form_invalid(form)


    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''A view to update a Profile'''
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''A view to delete a StatusMessage and remove it from the database'''
    
    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'status'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this status
        pk = self.kwargs.get('pk')
        status = StatusMessage.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # find the profile to which this status is related by FK
        profile = status.profile
        
        # reverse to show the article page
        return reverse('profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 

class UpdateStatusView(LoginRequiredMixin, UpdateView):
    '''A view to update a status message'''
    form_class = UpdateStatusForm
    template_name = "mini_fb/update_status_form.html"
    model = StatusMessage

    def form_valid(self, form):
        # save the status message to database
        sm = form.save()
        
        # read the file from the form:
        files = self.request.FILES.getlist('files')

        # read the deleted files from the form:
        deleted = self.request.POST.getlist('delete_images')

        # if not files:
        #     print("No files uploaded")
        # else:
        #     print(f"Files uploaded: {(files)}")

        if deleted:
            for d in deleted:
                image = Image.objects.get(pk=d)
                image.delete()  

        for file in files:
            image = Image.objects.create(status=sm, image_file=file)
            image.save()  

        return super().form_valid(form)
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    

class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        # profile_pk = kwargs.get('pk')
        other_profile_pk = kwargs.get('other_pk')
        
        try:
            # profile = Profile.objects.get(pk=profile_pk)
            profile = Profile.objects.get(user=self.request.user)
            # profile = Profile.objects.get(pk=self.kwargs['pk'])

            other_profile = Profile.objects.get(pk=other_profile_pk)
        except Profile.DoesNotExist:
            raise ValueError("Profile does not exist")

        # Call the add_friend method
        profile.add_friend(other_profile)
        
        # Redirect back to the profile page
        return redirect('profile', pk=profile.pk)
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'  # This is the context variable you'll use in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()  # Add friend suggestions to context
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()  # Get the Profile object
        context['news_feed'] = profile.get_news_feed()  # Get news feed
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login') 
    
    def get_object(self):
        return Profile.objects.get(user=self.request.user)
