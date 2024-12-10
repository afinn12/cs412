## Create View
# mini_fb/views.py
# Define the views for the mini_fb app:
#from django.shortcuts import render
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from .models import *
from django.views.generic import View, ListView, DetailView, CreateView
from django.urls import reverse
from django.shortcuts import redirect
from typing import Any
from django.views.generic.edit import UpdateView ## add UpdateView to list of imports
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import *

# Create your views here.

# Show All Accounts
class ShowAllAccounts(LoginRequiredMixin, ListView):
    '''Create a subclass of ListView to display all accounts.'''
    model = Account # retrieve objects of type Account from the database
    template_name = 'recipe/show_all_accounts.html'
    context_object_name = 'accounts' # how to find the data in the template file

    def dispatch(self, request):
        '''add this method to show/debug logged in user'''
        # print(f"Logged in user: request.user={request.user}")
        # print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        # print(f"Logged in user: request.user.account={hasattr(request.user, 'Account')}")

        return super().dispatch(request)
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
    
# Show all database recipes
class ShowAllDBRecipes(ListView):
    '''Create a subclass of ListView to display all accounts.'''
    model = DBRecipe # retrieve objects of type Account from the database
    template_name = 'recipe/show_all_dbrecipes.html'
    context_object_name = 'dbrecipes' # how to find the data in the template file
    paginate_by = 18

    def dispatch(self, request):
        '''add this method to show/debug logged in user'''
        return super().dispatch(request)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        if self.request.user.is_authenticated:
            context['user_account'] =  Account.objects.get(user=self.request.user)

        return context

# Show all user recipes 
class ShowUserRecipes(LoginRequiredMixin, ListView):
    '''Create a subclass of ListView to display all accounts.'''
    model = UserRecipe # retrieve objects of type Account from the database
    template_name = 'recipe/show_explore.html'
    context_object_name = 'userrecipes' # how to find the data in the template file

    def dispatch(self, request):
        # '''add this method to show/debug logged in user'''
        # print(f"Logged in user: request.user={request.user}")
        # print(f"Logged in user: request.user.is_authenticated={request.user.is_authenticated}")
        # print(f"Logged in user: request.user.account={hasattr(request.user, 'Account')}")

        return super().dispatch(request)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        context['user_account'] =  Account.objects.get(user=self.request.user)

        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
# Register a new user
class RegistrationView(CreateView):
    '''Handle registration of new Users.'''

    template_name = 'recipe/recipe_register.html' # we write this
    form_class = UserCreationForm # built-in from django.contrib.auth.forms

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        '''Handle the User creation form submission.'''
        
        # if we received an HTTP POST, we handle it 
        if self.request.POST:
            
            # reconstruct the UserCreateForm from the POST data
            form = UserCreationForm(self.request.POST)

            if not form.is_valid():
                print(f"form.errors={form.errors}")

                # let CreateView.dispatch handle the problem
                return super().dispatch(request, *args, **kwargs)

            # save the form, which creates a new User
            user = form.save() # this will commit the insert to the database
            # print(f"RegistrationView.dispatch: created user {user}.")

            # log the User in
            login(self.request, user)

            # return a response:
            return redirect(reverse('create_account'))


        # let CreateView.dispatch handle the HTTP GET request
        return super().dispatch(request, *args, **kwargs)
    
# Create an account for a new user
class CreateAccountView(CreateView):
    '''
    A view to create a StatusMessage on a Account.
    on GET: send back the form to display
    on POST: read/process the form, and save new StatusMessage to the database
    '''

    form_class = CreateAccountForm
    template_name = "recipe/create_account_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # get the context data from the superclass
        context =  super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 


    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        # find the Account identified by the PK from the URL pattern
        return reverse('account', kwargs={'pk': self.object.pk})


    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''

        # If already have a user account, create a account
        if self.request.user.is_authenticated:  
            form.instance.user = self.request.user 
            return super().form_valid(form)
        

        # Reconstruct the UserCreationForm from the request data
        user_form = UserCreationForm(self.request.POST)
        
        if user_form.is_valid() and form.is_valid(): 
            
            user_instance = user_form.save()
            form.instance.user = user_instance  
            login(self.request, user_instance)
            return super().form_valid(form)

        return self.form_invalid(form)


# Show the details of an account
class ShowAccountView(LoginRequiredMixin, DetailView):
    '''Display one Account selected by PK'''
    model = Account # the model to display
    template_name = "recipe/show_account.html"
    context_object_name = "account"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        account = Account.objects.get(user=self.request.user)  
        context['user_account'] = account 

        if account != self.object: 
            context['account_likes'] = account.get_accountlikes(self.object) 

        return context

    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 

# Show the details of a user recipe
class ShowUserRecipeView(LoginRequiredMixin, DetailView):
    '''Display one Account selected by PK'''
    model = UserRecipe # the model to display
    template_name = "recipe/show_userrecipe.html"
    context_object_name = "recipe"

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        context['user_account'] =  Account.objects.get(user=self.request.user)

        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 

# Show the details of a database recipe
class ShowDBRecipeView(DetailView):
    '''Display one Account selected by PK'''
    model = DBRecipe # the model to display
    template_name = "recipe/show_dbrecipe.html"
    context_object_name = "recipe"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        context['user_account'] =  Account.objects.get(user=self.request.user)

        return context

# Allows the user to create recipes
class CreateRecipeView(LoginRequiredMixin, CreateView):
    '''
    A view to create a StatusMessage on a Account.
    on GET: send back the form to display
    on POST: read/process the form, and save new StatusMessage to the database
    '''

    form_class = CreateRecipeForm
    template_name = "recipe/create_recipe_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # get the context data from the sueprclass (the account)
        context =  super().get_context_data(**kwargs)
        context['account']  = Account.objects.get(user=self.request.user)
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        return reverse('account', kwargs={'pk':self.object.author.pk})

    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''

        # find the account based on the pk in the URL 
        account = Account.objects.get(user=self.request.user)

        # attach this account to the recipe author
        form.instance.author = account 

        # save the recipe to database
        r = form.save()
        
        # process any images
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image.objects.create(recipe=r, image_file=file)
            image.save()  

        # delegate work to superclass version of this method
        return super().form_valid(form)   
     
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 

# Allows a user to delete their recipes
class DeleteRecipeView(LoginRequiredMixin, DeleteView):
    '''A view to delete a StatusMessage and remove it from the database'''
    
    template_name = "recipe/delete_recipe_form.html"
    model = UserRecipe
    context_object_name = 'recipe'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this recipe
        pk = self.kwargs.get('pk')
        recipe = UserRecipe.objects.filter(pk=pk).first() # get one object from QuerySet
        
        # go back to the account page
        return reverse('account', kwargs={'pk':recipe.author.pk})
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 

# Allows a user to update their recipes
class UpdateRecipeView(LoginRequiredMixin, UpdateView):
    '''A view to update a status message'''
    form_class = UpdateRecipeForm
    template_name = "recipe/update_recipe_form.html"
    model = UserRecipe
    context_object_name = 'recipe'


    def form_valid(self, form):
        r = form.save()
        
        # read the file from the form:
        files = self.request.FILES.getlist('files')

        # delete the selected images from the recipe:
        deleted = self.request.POST.getlist('delete_images')
        if deleted:
            for d in deleted:
                image = Image.objects.get(pk=d)
                image.delete()  

        # add any new images
        for file in files:
            image = Image.objects.create(recipe=r, image_file=file)
            image.save()  

        # delegate work to superclass version of this method
        return super().form_valid(form)
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
# Allows a user to update their account
class UpdateAccountView(LoginRequiredMixin, UpdateView):
    '''A view to update a Account'''
    form_class = UpdateAccountForm
    template_name = "recipe/update_account_form.html"
    model = Account

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
    def get_object(self):
        return Account.objects.get(user=self.request.user)
    

# The view for a user's friend suggestions
class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'recipe/friend_suggestions.html'
    context_object_name = 'account' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions() 
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
    def get_object(self):
        return Account.objects.get(user=self.request.user)

#
# The view for a user's friend feed (their recipes and their friends')
class ShowFriendsFeedView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'recipe/friends_feed.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.get_object()  
        context['user_account'] = Account.objects.get(user=self.request.user)
        context['friends_feed'] = account.get_friends_feed() 
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
    def get_object(self):
        return Account.objects.get(user=self.request.user)

# Allows users to add friends
class CreateFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        other_account_pk = kwargs.get('other_pk')
        # Check that the accounts exist
        try:
            account = Account.objects.get(user=self.request.user)
            other_account = Account.objects.get(pk=other_account_pk)
        except Account.DoesNotExist:
            raise ValueError("Account does not exist")

        # Call the add_friend method, has error checking
        account.add_friend(other_account)
        
        # Redirect back to the account page
        return redirect('account', pk=other_account.pk)
    
    def get_object(self):
        return Account.objects.get(user=self.request.user)

# Allows users to remove friends
class RemoveFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        other_account_pk = kwargs.get('other_pk') 
        # get the accounts if they exist
        try:
            account = Account.objects.get(user=self.request.user) 
            other_account = Account.objects.get(pk=other_account_pk)
        except Account.DoesNotExist:
            raise ValueError("Account does not exist")


        # delete the friendship if it exists
        try:
            friendship = Friend.objects.filter(account1=account, account2=other_account).first() or \
                Friend.objects.filter(account1=other_account, account2=account).first()
            friendship.delete() 
        except Friend.DoesNotExist:
            raise ValueError("Friendship does not exist")

        # Redirect/stay on the friend's account
        return redirect('account', pk=other_account.pk)

    def get_object(self):
        return Account.objects.get(user=self.request.user)
    
# Show all the recipes a user likes
class ShowLikesView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'recipe/likes.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = self.get_object() 
        # pass the likes as a context variable
        context['userlikes'] = account.get_userlikes()  
        context['dblikes'] = account.get_dblikes() 
        context['user_account'] =  Account.objects.get(user=self.request.user)
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
    def get_object(self):
        return Account.objects.get(pk=self.kwargs.get('pk'))

# Allows a user to like a user recipe
class CreateUserLikeView(View):
    def dispatch(self, request, *args, **kwargs):
        recipe_pk = kwargs.get('other_pk')
        # Get the acccout/recipe for the relationship if it exists
        try:
            account = Account.objects.get(user=self.request.user)
            recipe = UserRecipe.objects.get(pk=recipe_pk)
        except (Account.DoesNotExist, UserRecipe.DoesNotExist):
            raise ValueError("Account or Recipe doesn't exist")

        # like the recipe, this error checks if exists
        recipe.add_userlike(account)
        
        # Redirect/stay on the friend's account
        next_url = request.GET.get('next')

        # use next to stay on the same page, but reload it
        if next_url:
            return redirect(next_url)

        # else, go to the recipe's page
        return redirect('recipe', pk=recipe.pk)

    
    def get_object(self):
        return Account.objects.get(user=self.request.user)
    
# Allows a user to unlike a user recipe
class RemoveUserLikeView(View):
    def dispatch(self, request, *args, **kwargs):
        recipe = kwargs.get('other_pk') 
        try:
            account = Account.objects.get(user=self.request.user) 
            recipe = UserRecipe.objects.get(pk=recipe)
        except (Account.DoesNotExist, UserRecipe.DoesNotExist):
            raise ValueError("Account or Recipe doesn't exist")


        # delete the like if it exists
        try:
            like = Like.objects.filter(account=account, user_recipe=recipe).first()
            like.delete()
        except Like.DoesNotExist:
            raise ValueError("Like does not exist")

        # Redirect/stay on the friend's account
        next_url = request.GET.get('next')

        # use next to stay on the same page, but reload it
        if next_url:
            return redirect(next_url)

        # else, go to the recipe's page
        return redirect('recipe', pk=recipe.pk)

    def get_object(self):
        return Account.objects.get(user=self.request.user)
    

# Allows a user to like a database recipe
class CreateDBLikeView(View):
    def dispatch(self, request, *args, **kwargs):
        recipe_pk = kwargs.get('other_pk')
        # Get the acccout/recipe for the relationship if it exists
        try:
            account = Account.objects.get(user=self.request.user)
            recipe = DBRecipe.objects.get(pk=recipe_pk)
        except (Account.DoesNotExist, DBRecipe.DoesNotExist):
            raise ValueError("Account or Recipe doesn't exist")

        # like the recipe, this error checks if exists
        recipe.add_dblike(account)
        
        # return HttpResponse(status=204) 
        # return HttpResponse('<script>window.location.reload();</script>', content_type='text/html')
        next_url = request.GET.get('next')

        # use next to stay on the same page, but reload it
        if next_url:
            return redirect(next_url)

        # else, go to the recipe's page
        return redirect('dbrecipe', pk=recipe.pk)
        # return redirect(request.path)

    
    def get_object(self):
        return Account.objects.get(user=self.request.user)
    
# Allows a user to unlike a database recipe
class RemoveDBLikeView(View):
    def dispatch(self, request, *args, **kwargs):
        recipe = kwargs.get('other_pk') 
        try:
            account = Account.objects.get(user=self.request.user) 
            recipe = DBRecipe.objects.get(pk=recipe)
        except (Account.DoesNotExist, DBRecipe.DoesNotExist):
            raise ValueError("Account or Recipe doesn't exist")

        # delete the like if it exists
        try:
            like = Like.objects.filter(account=account, db_recipe=recipe).first()
            like.delete()
        except Like.DoesNotExist:
            raise ValueError("Like does not exist")

        next_url = request.GET.get('next')

        # se next to stay on the same page, but reload it
        if next_url:
            return redirect(next_url)

        # else, go to the recipe's page
        return redirect('dbrecipe', pk=recipe.pk)

    def get_object(self):
        return Account.objects.get(user=self.request.user)
    
# Shows all cookbooks for an account
class ShowAllCookbooksView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'recipe/show_all_cookbooks.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        account = self.get_object()  
        context['cookbooks'] = account.get_cookbooks()  
        context['user_account'] =  Account.objects.get(user=self.request.user)

        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
    def get_object(self):
        return Account.objects.get(pk=self.kwargs.get('pk'))
    
# shows all recipes in a given cookbook
class ShowCookbookView(LoginRequiredMixin, DetailView):
    model = Cookbook
    template_name = 'recipe/show_cookbook.html'
    context_object_name = 'cookbook'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cookbook = self.get_object()
        context['account'] =  cookbook.account
        context['userrecipes'] = cookbook.get_userrecipes()  
        context['dbrecipes'] = cookbook.get_dbrecipes() 
        context['user_account'] =  Account.objects.get(user=self.request.user)

        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
    def get_object(self):
        return Cookbook.objects.get(pk=self.kwargs.get('pk'))
    
# Allows a user to create a new cookbook
class CreateCookbookView(LoginRequiredMixin, CreateView):
    '''
    A view to create a StatusMessage on a Account.
    on GET: send back the form to display
    on POST: read/process the form, and save new StatusMessage to the database
    '''

    form_class = CreateCookbookForm
    template_name = "recipe/create_cookbook_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        # get the context data from the sueprclass
        context =  super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        context['account'] = account
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''
        return reverse('all_cookbooks', kwargs={'pk':self.object.account.pk})

    def form_valid(self, form):
        '''This method is called after the form is validated, 
        before saving data to the database.'''

        account = Account.objects.get(user=self.request.user)

        form.instance.account = account 

        r = form.save()
        
        files = self.request.FILES.getlist('files')

        for file in files:
            image = Image.objects.create(recipe=r, image_file=file)
            image.save()  

        # delegate work to superclass version of this method
        return super().form_valid(form)   
     
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    
# Allows a user to update a new cookbook
class UpdateCookbookView(LoginRequiredMixin, UpdateView):
    '''A view to update a status message'''
    form_class = UpdateCookbookForm
    template_name = "recipe/update_cookbook_form.html"
    model = Cookbook
    context_object_name = 'cookbook'


    def form_valid(self, form):
        # save the cookbook to database
        form.save()

        return super().form_valid(form)
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    

# Allows a user to delete a new cookbook
class DeleteCookbookView(LoginRequiredMixin, DeleteView):
    '''A view to delete a cookbook and remove it from the database'''
    
    template_name = "recipe/delete_cookbook_form.html"
    model = Cookbook
    context_object_name = 'cookbook'
    
    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''
        # get the pk for this status
        pk = self.kwargs.get('pk')
        cookbook = Cookbook.objects.filter(pk=pk).first()
        
        # reverse to show the article page
        return reverse('all_cookbooks', kwargs={'pk':cookbook.account.pk})
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    


# The view for searching db and user recipes
class RecipeSearchListView(LoginRequiredMixin, ListView):
    """View to show a list of filtered recipes."""
    template_name = 'recipe/results.html'  
    context_object_name = 'recipes'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_account'] =  Account.objects.get(user=self.request.user)
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 

    def get_queryset(self):
        """Filter recipes based on query parameters."""
        qs_user = UserRecipe.objects.all()
        qs_db = DBRecipe.objects.all()

        # title filter
        title = self.request.GET.get('title')
        if title:
            parts = title.split(',')
            for p in parts:
                qs_user = qs_user.filter(title__icontains=p.strip())
                qs_db = qs_db.filter(title__icontains=p.strip())

        # description filter
        description = self.request.GET.get('description')
        if description:
            parts = description.split(',')
            for p in parts:
                qs_user = qs_user.filter(description__icontains=p.strip())
                qs_db = qs_db.filter(description__icontains=p.strip())

        # ingredients filter
        ingredients = self.request.GET.get('ingredients')
        if ingredients:
            parts = ingredients.split(',')
            for p in parts:
                qs_user = qs_user.filter(ingredients__icontains=p.strip())
                qs_db = qs_db.filter(ingredients__icontains=p.strip())


        # author filter
        author = self.request.GET.get('author')
        if author:
            parts = author.split(',')
            for p in parts:
                qs_user = qs_user.filter(author__first__icontains=p.strip()) | qs_user.filter(author__last__icontains=p.strip())
                qs_db = qs_db.filter(author__icontains=p.strip())

        type = self.request.GET.get('type')
        if type:
            if (type.strip() == "user"):
                return list(qs_user)
            else:
                return list(qs_db)

        return list(qs_user) + list(qs_db)
    
# Allows a user to add user recipes to their cookbook
class AddUserToCookbookView(LoginRequiredMixin, DetailView):
    '''A view to delete a StatusMessage and remove it from the database'''
    
    template_name = "recipe/add_user_cookbook_form.html"
    model = UserRecipe
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        context['user_account'] =  account
        context['user_cookbooks'] =  account.get_cookbooks
        
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    

    def post(self, request, *args, **kwargs):
        # When the form is submitted, this method is called
        # It's essentially form_valid without django's forms

        if self.request.POST:
            cookbook = Cookbook.objects.get(pk=self.request.POST.get('cookbook'))
            userrecipe = UserRecipe.objects.get(pk=self.kwargs['pk'])

            if userrecipe:
                if cookbook.user_recipes.filter(pk=userrecipe.pk):
                    raise ValueError("Recipe already in this cookbook.")
                # add the recipe if not already in cookbook
                cookbook.user_recipes.add(userrecipe)
            else:
                raise ValueError("Invalid Recipe")

            # delegate work to superclass version of this method
            return redirect(reverse('cookbook', kwargs={'pk': self.request.POST.get('cookbook')}))
        
# Allows a user to remove user recipes to their cookbook
class RemoveUserToCookbookView(View):
    def dispatch(self, request, *args, **kwargs):

        try:
            cookbook = Cookbook.objects.get(pk=self.request.POST.get('cookbook'))
            userrecipe = UserRecipe.objects.get(pk=self.kwargs['pk'])
        except (Cookbook.DoesNotExist, UserRecipe.DoesNotExist):
            raise ValueError("Cookbook or Recipe doesn't exist")


        # Delete the recipe if its in the cookbook
        if userrecipe:
            if cookbook.user_recipes.filter(pk=userrecipe.pk):
                cookbook.user_recipes.remove(userrecipe)
            else:
                raise ValueError("Recipe is not in this cookbook.")
        else:
            raise ValueError("Invalid Recipe")

        # Direct back to the cookbook
        return redirect('cookbook', pk=cookbook.pk)

    def get_object(self):
        return Account.objects.get(user=self.request.user)
    
# Allows a user to add database recipes to their cookbook
class AddDBToCookbookView(LoginRequiredMixin, DetailView):
    
    template_name = "recipe/add_db_cookbook_form.html"
    model = DBRecipe
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = Account.objects.get(user=self.request.user)
        context['user_account'] =  account
        context['user_cookbooks'] =  account.get_cookbooks
        
        return context

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('recipe_login') 
    

    def post(self, request, *args, **kwargs):
        # When the form is submitted, this method is called
        # It's essentially form_valid without django's forms

        if self.request.POST:
            cookbook = Cookbook.objects.get(pk=self.request.POST.get('cookbook'))
            dbrecipe = DBRecipe.objects.get(pk=self.kwargs['pk'])

            if dbrecipe:
                if cookbook.db_recipes.filter(pk=dbrecipe.pk):
                    raise ValueError("Recipe already in this cookbook.")
                # add the recipe if not already in cookbook
                cookbook.db_recipes.add(dbrecipe)
            else:
                raise ValueError("Invalid Recipe")

            # delegate work to superclass version of this method
            return redirect(reverse('cookbook', kwargs={'pk': self.request.POST.get('cookbook')}))


# Allows a user to remove database recipes from their cookbook
class RemoveDBToCookbookView(View):    
    def dispatch(self, request, *args, **kwargs):
        try:
            cookbook = Cookbook.objects.get(pk=self.request.POST.get('cookbook'))
            dbrecipe = DBRecipe.objects.get(pk=self.kwargs['pk'])
        except (Cookbook.DoesNotExist, DBRecipe.DoesNotExist):
            raise ValueError("Cookbook or Recipe doesn't exist")


        # Delete the friendship if it exists, otherwise raise an error
        if dbrecipe:
            if cookbook.db_recipes.filter(pk=dbrecipe.pk):
                cookbook.db_recipes.remove(dbrecipe)
            else:
                raise ValueError("Recipe is not in this cookbook.")
        else:
            raise ValueError("Invalid Recipe")

        # Direct back to the cookbook
        return redirect('cookbook', pk=cookbook.pk)

    def get_object(self):
        return Account.objects.get(user=self.request.user)
    
# Shows all the accounts that like the user's recipe
class ShowAllLikes(LoginRequiredMixin, ListView):
    '''Create a subclass of ListView to display all accounts who like a specific UserRecipe.'''

    model = Account 
    template_name = 'recipe/show_likes.html'
    context_object_name = 'accounts'  

    def get_login_url(self) -> str:
        '''Return the URL required for login'''
        return reverse('recipe_login')

    def get_queryset(self):
        '''Return the list of accounts who liked the UserRecipe with pk = self.kwargs['pk'].'''
        user_recipe = UserRecipe.objects.get(pk=self.kwargs['pk']) 
        # get all likes for the given recipe
        likes = Like.objects.filter(user_recipe=user_recipe)
        # return all the accounts associated with these likes
        return [like.account for like in likes]  

    def get_context_data(self, **kwargs):
        '''Add the UserRecipe instance to the context to display the recipe's details.'''
        context = super().get_context_data(**kwargs)
        user_recipe = UserRecipe.objects.get(pk=self.kwargs['pk'])
        context['user_recipe'] = user_recipe
        return context
