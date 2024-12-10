from django import forms
from .models import Account, UserRecipe, Cookbook

class CreateAccountForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''

    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Account
        fields = ['first', 'last', 'dob', 'email', 'image_url']  # which fields from model should we use
        labels = {
            'first': 'First Name:',
            'last': 'Last Name:',
            'dob': 'Date of Birth:',
            'email': 'Email:',
            'image_url' : 'Image URL:',
        }

class CreateRecipeForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = UserRecipe
        fields = ['title', 'description', 'ingredients', 'instructions']  # which fields from model should we use


class UpdateAccountForm (forms.ModelForm):
    '''A form to update a Profile to the database.'''
    class Meta:
        '''associate this form with the Profile model.'''
        model = Account
        fields = ['first', 'last', 'dob', 'email', 'image_url']  # which fields from model should we use
        labels = {
            'first': 'First Name:',
            'last': 'Last Name:',
            'dob': 'Date of Birth:',
            'email': 'Email:',
            'image_url' : 'Image URL:',
        }


class UpdateRecipeForm (forms.ModelForm):
    '''A form to update a Recipe to the database.'''

    class Meta:
        '''associate this form with the status model.'''
        model = UserRecipe
        fields = ['title', 'description', 'ingredients', 'instructions']  # which fields from model should we use


class CreateCookbookForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''
    class Meta:
        '''associate this form with the Comment model; select fields.'''
        model = Cookbook
        fields = ['name', 'user_recipes', 'db_recipes']  # which fields from model should we use

class UpdateCookbookForm (forms.ModelForm):
    '''A form to update a Recipe to the database.'''

    class Meta:
        '''associate this form with the status model.'''
        model = Cookbook
        fields = ['name', 'user_recipes', 'db_recipes'] # which fields from model should we use
