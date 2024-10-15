## write the CreateCommentForm
# blog/forms.py
from django import forms
from .models import StatusMessage

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = StatusMessage
        fields = ['profile', 'message']  # which fields from model should we use