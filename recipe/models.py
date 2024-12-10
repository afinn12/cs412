from django.db import models
from django.contrib.auth.models import User 
from django.urls import reverse
import json


# Create your models here.

class Account(models.Model):
    '''Encapsulate the idea of an Account'''

    # every Account has one User:
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # data attributes of a Account:
    first = models.CharField(max_length=64)
    last = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    dob = models.DateField(blank=False)
    image_url = models.URLField(blank=True)
    
    def __str__(self):
        '''Return a string representation of this Account object.'''
        return f'{self.first} {self.last}'
    
    def get_user(self):
        '''Return a list of possible friends for this account.'''
        # Get all friends of the current account
        user = User.objects.filter(user=self)

        return user
    
    def get_recipes(self):
        '''Return all of the recipes created by this account.'''
        recipes = UserRecipe.objects.filter(author=self)
        return recipes
    
    def get_userlikes(self):
        '''Return all of the userrecipes liked by this account.'''
        # Get all likes by this account
        likes = Like.objects.filter(account=self)
        recipes= []
        for like in likes:
            if like.user_recipe:
                recipes.append(like.user_recipe)

        return recipes
    
    def get_dblikes(self):
        '''Return all of the dbrecipes liked by this account.'''
        # Get all likes by this account
        likes = Like.objects.filter(account=self)
        recipes= []
        for like in likes:
            if like.db_recipe:
                recipes.append(like.db_recipe)

        return recipes
    
    def get_cookbooks(self):
        '''Return all of the cookbooks created by this account.'''
        return Cookbook.objects.filter(account=self)
    
    def get_friends(self):
        '''Return a list of accounts that are friends with this account.'''

        # Retrieve Friend instances where this account is either account1 or account2
        account1 = Friend.objects.filter(account1=self)
        account2 = Friend.objects.filter(account2=self)

        # Collect all the friend accounts (either from account1 or account2)
        friend_accounts = [
            friend.account2 for friend in account1
        ] + [
            friend.account1 for friend in account2
        ]

        return friend_accounts
    
    def add_friend(self, other):
        """Add a friendship if it doesn't already exist and is not with self."""
        # make sure it's with a different person
        if self == other:
            raise ValueError("You cannot add yourself as a friend.")

        existing = Friend.objects.filter(
            account1=self, account2=other
        ) | Friend.objects.filter(
            account1=other, account2=self
        )

        # make sure they're not already friends
        if existing:
            raise ValueError("Friendship already exists.")

        # Create the new Friend relationship
        Friend.objects.create(account1=self, account2=other)

    def get_friend_suggestions(self):
        '''Return a list of possible friends for this account.'''
        # Get all friends of the current account
        friends1 = Friend.objects.filter(account1=self).values_list('account2', flat=True)
        friends2 = Friend.objects.filter(account2=self).values_list('account1', flat=True)

        friends = list(friends1) + list(friends2)

        # Get all accounts that are not friends and not the current account
        friend_suggestions = Account.objects.exclude(
            id__in=friends  # Exclude current friends
        ).exclude(
            id=self.id      # Exclude the current account
        )

        return friend_suggestions
    
    def get_friends_feed(self):
        '''Return a list of recipes of this account and its friends.'''
        # Get the current account's recipes
        own = UserRecipe.objects.filter(author=self)

        # Get the friends of this account
        friends = self.get_friends() 

        # Get recipes from friends
        other = UserRecipe.objects.filter(author__in=friends)

        # Combine own messages and friends' messages
        all_messages = own | other 

        # Return combined messages sorted by timestamp (most recent first)
        return all_messages.order_by('-timestamp')

    def get_absolute_url(self):
        '''Return the URL that will display an instance of this object.'''
        # self.pk is the primary key to this Profile instance
        return reverse('account', kwargs={'pk': self.pk})
    
    
    def get_accountlikes(self, account):
        '''Return all of the userrecipes liked by this account, created by the given account.'''
        # Get all likes by this account
        likes = Like.objects.filter(account=self)
        recipes = []
        for like in likes:
            if like.user_recipe and like.user_recipe.author == account:
                recipes.append(like.user_recipe)
        return recipes

 
class UserRecipe(models.Model):
    '''Encapsulate the idea of a recipe on an Account.'''
    
    # data attributes of a Recipe:
    author = models.ForeignKey("Account", on_delete=models.CASCADE)
    title = models.TextField(blank=False)
    ingredients = models.TextField(blank=False)
    instructions = models.TextField(blank=False)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this recipe object.'''
        return f'{self.title}'
    
    def get_images(self):
        '''Return all of the images about this recipe.'''
        image = Image.objects.filter(recipe=self)
        return image
    
    def get_absolute_url(self):
        '''Return the URL that will display an instance of this object.'''
        # self.pk is the primary key to this Profile instance
        return reverse('recipe', kwargs={'pk': self.author.pk})
    
    def add_userlike(self, account):
        """Add a like to this recipe"""
        if self.author == account:
            raise ValueError("You cannot like your own recipes.")

        existing = Like.objects.filter(account=account, user_recipe=self)

        if existing:
            raise ValueError("Like already exists.")

        # Create the new Friend relationship
        Like.objects.create(account=account, user_recipe=self)

    def get_likes(self):
        '''Return all likes by users.'''
        # Get all likes by this account
        likes = Like.objects.filter(user_recipe=self)
        return likes
    
    def get_cookbooks(self):
        '''Return all of the cookbooks created by this account.'''
        books = Cookbook.objects.filter(user_recipes=self)
        return books

    
class DBRecipe(models.Model):
    '''Encapsulate the idea of a recipe from the database.'''
    
    # data attributes of a Recipe:
    author = models.TextField(blank=False)
    title = models.TextField(blank=False)
    ingredients = models.TextField(blank=False)
    instructions = models.TextField(blank=False)
    description = models.TextField(blank=False)

    # Link to source
    url = models.URLField(blank=True)

    
    def __str__(self):
        '''Return a string representation of this recipe object.'''
        return f'{self.title}'
        # return (
        # f"Author: {self.author}\n"
        # f"Title: {self.title}\n"
        # f"Ingredients: {self.ingredients}\n"
        # f"Instructions: {self.instructions}\n\n")

    def get_absolute_url(self):
        '''Return the URL that will display an instance of this object.'''
        # self.pk is the primary key to this Profile instance
        return reverse('dbrecipe', kwargs={'pk': self.author.pk})

    def add_dblike(self, account):
        """Add a like if it doesn't already exist to this recipe."""
        if self.author == account:
            raise ValueError("You cannot like your own recipes.")

        existing = Like.objects.filter(account=account, db_recipe=self)

        if existing:
            raise ValueError("Like already exists.")

        # Create the new Friend relationship
        Like.objects.create(account=account, db_recipe=self)

    def get_likes(self):
        '''Return all the likes by users.'''
        # Get all likes by this account
        likes = Like.objects.filter(db_recipe=self)
        
        return likes
    
    def get_cookbooks(self):
        '''Return all of the cookbooks created by this account.'''
        books = Cookbook.objects.filter(db_recipes=self)

        return books


class Image(models.Model):
    '''Encapsulate the idea of an Image on a UserRecipe.'''

    recipe = models.ForeignKey("UserRecipe", on_delete=models.CASCADE)
    image_file = models.ImageField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Image object.'''
        return f'{self.image_file}'
        

class Friend(models.Model):
    '''Encapsulate the idea of a friendship between two Accounts.'''
    
    account1 = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="account1")
    account2 = models.ForeignKey("Account", on_delete=models.CASCADE, related_name="account2")
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        '''Return a string representation of this Friend object.'''
        return f'{self.account1.first} {self.account1.last} & {self.account2.first} {self.account2.last}'


class Like(models.Model):
    '''Encapsulate the idea of a Like on a Recipe.'''

    account = models.ForeignKey("Account", on_delete=models.CASCADE, blank=False)
    # error checking for one to be filled but not the other below
    db_recipe = models.ForeignKey("DBRecipe", on_delete=models.CASCADE, blank=True, null=True)
    user_recipe = models.ForeignKey("UserRecipe", on_delete=models.CASCADE, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Like object.'''
        return f'{self.account} liked {self.db_recipe or self.user_recipe}'
    
    def save(self, *args, **kwargs):
        # Make sure ONLY one field is filled for the recipes, not both or neither.
        if not self.db_recipe and not self.user_recipe:
            raise ValueError("Either 'db_recipe' or 'user_recipe' must be filled.")
        if self.db_recipe and self.user_recipe:
            raise ValueError("Both 'db_recipe' and 'user_recipe' cannot be filled.")

        super().save(*args, **kwargs)


class Cookbook(models.Model):
    '''Encapsulate the idea of a cookbook belonging to an account with both DBRecipes and UserRecipes.'''

    name = models.CharField(max_length=64)
    account = models.ForeignKey("Account", on_delete=models.CASCADE)
    db_recipes = models.ManyToManyField("DBRecipe", blank=True)
    user_recipes = models.ManyToManyField("UserRecipe", blank=True)


    def __str__(self):
        '''Return a string representation of the Cookbook, which is number of recipes types.'''
        '''Name is accessed through the field.'''
        
        return f"({self.db_recipes.count()} DBRecipes, {self.user_recipes.count()} UserRecipes)"
    
    def get_absolute_url(self):
        '''Return the URL that will display an instance of this object.'''
        # self.pk is the primary key to this Profile instance
        return reverse('cookbook', kwargs={'pk': self.pk})
    
    def get_userrecipes(self):
        '''Return all of the userrecipes in this cookbook.'''
        # Get all userrecipes in this cookbook
        recipes = recipes = self.user_recipes.all()  
        return recipes
    
    def get_dbrecipes(self):
        '''Return all of the dbrecipes in this cookbook.'''
        # Get all dbrecipes in this cookbook
        recipes = recipes = self.db_recipes.all()  
        return recipes


def load_data():
    '''Load data records from the json file into model instances.'''
    # Delete all DBRecipes to clear the database
    DBRecipe.objects.all().delete()

    filename = "C:\\Users\\Anna\\Downloads\\cs412\\recipes.json"
    f = open(filename, 'r')

    data = json.load(f)

    # iterate through each recipe 
    for recipe in data:
        try:
            # create a DBRecipe instance
            result = DBRecipe(
                title=recipe.get("Name", "").strip(),
                url=recipe.get("url", "").strip(),
                author=recipe.get("Author", "Unknown"),
                description=recipe.get("Description",),
                ingredients="\n".join(recipe.get("Ingredients", [])),
                instructions="\n".join(recipe.get("Method", [])),
            )
            # Commit to the database
            result.save()  
        
        except Exception as e:
            print(f"Exception on {recipe}: {e}")

