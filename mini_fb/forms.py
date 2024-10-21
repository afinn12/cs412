## write the CreateCommentForm
# blog/forms.py
from django import forms
from .models import Profile, StatusMessage

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = StatusMessage
        fields = ['message']  # which fields from model should we use


class CreateProfileForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''

    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Profile
        fields = ['first', 'last', 'city', 'email', 'image_url']  # which fields from model should we use
        labels = {
            'first': 'First Name',
            'last': 'Last Name',
        }

class UpdateProfileForm (forms.ModelForm):
    '''A form to update a Profile to the database.'''
    class Meta:
        '''associate this form with the Profile model.'''
        model = Profile
        fields = ['first', 'last', 'city', 'email', 'image_url']  # which fields from model should we use
        labels = {
            'first': 'First Name',
            'last': 'Last Name',
        }


class UpdateStatusForm (forms.ModelForm):
    '''A form to update a status to the database.'''
    # images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)


    class Meta:
        '''associate this form with the status model.'''
        model = StatusMessage
        fields = ['message'] 