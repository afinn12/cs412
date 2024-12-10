
## formdata/urls.py
## define the URLs for this app

from django.urls import path
from django.contrib.auth import views as auth_views
# from .views import ShowAllRecipes

from .views import *

# define a list of valid URL patterns:
urlpatterns = [
    path('', ShowUserRecipes.as_view(), name='show_explore'), 
    path('show_all_dbrecipes', ShowAllDBRecipes.as_view(), name='show_all_dbrecipes'),
    path('show_all_accounts', ShowAllAccounts.as_view(), name='show_all_accounts'),
    path('login/', auth_views.LoginView.as_view(template_name='recipe/recipe_login.html'), name='recipe_login'), 
    path('logout/', auth_views.LogoutView.as_view(template_name='recipe/recipe_logout.html'), name='recipe_logout'), 
    path('register/', RegistrationView.as_view(), name='recipe_register'),
    path('create_account/', CreateAccountView.as_view(), name="create_account"), 
    path('account/<int:pk>', ShowAccountView.as_view(), name="account"), 
    path('recipe/create_recipe', CreateRecipeView.as_view(), name="create_recipe"), 
    path('recipe/<int:pk>/delete', DeleteRecipeView.as_view(), name='delete_recipe'),
    path('status/<int:pk>/update', UpdateRecipeView.as_view(), name='update_recipe'),
    path('account/update', UpdateAccountView.as_view(), name="update_account"),
    path('recipe/<int:pk>', ShowUserRecipeView.as_view(), name="recipe"), 
    path('dbrecipe/<int:pk>', ShowDBRecipeView.as_view(), name="dbrecipe"), 
    path('friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='recipe_friend_suggestions'),
    path('friends_feed/', ShowFriendsFeedView.as_view(), name='friends_feed'),
    path('add_friend/<int:other_pk>/', CreateFriendView.as_view(), name='recipe_add_friend'),
    path('remove_friend/<int:other_pk>/', RemoveFriendView.as_view(), name='recipe_remove_friend'),
    path('add_userlike/<int:other_pk>/', CreateUserLikeView.as_view(), name='add_userlike'),
    path('remove_userlike/<int:other_pk>/', RemoveUserLikeView.as_view(), name='remove_userlike'),
    path('add_dblike/<int:other_pk>/', CreateDBLikeView.as_view(), name='add_dblike'),
    path('remove_dblike/<int:other_pk>/', RemoveDBLikeView.as_view(), name='remove_dblike'),
    path('account/<int:pk>/likes/', ShowLikesView.as_view(), name='likes'),
    path('account/<int:pk>/all_cookbooks/', ShowAllCookbooksView.as_view(), name='all_cookbooks'),
    path('cookbook/<int:pk>/', ShowCookbookView.as_view(), name='cookbook'),
    path('create_cookbook/', CreateCookbookView.as_view(), name="create_cookbook"), 
    path('cookbook/<int:pk>/update/', UpdateCookbookView.as_view(), name='update_cookbook'),
    path('cookbook/<int:pk>/delete/', DeleteCookbookView.as_view(), name='delete_cookbook'),
    path('search/', RecipeSearchListView.as_view(), name='search'),
    path('recipe/<int:pk>/add_user_cookbook', AddUserToCookbookView.as_view(), name='add_user_cookbook'),
    path('dbrecipe/<int:pk>/add_db_cookbook', AddDBToCookbookView.as_view(), name='add_db_cookbook'),
    path('recipe/<int:pk>/remove_user_cookbook', RemoveUserToCookbookView.as_view(), name='remove_user_cookbook'),
    path('dbrecipe/<int:pk>/remove_db_cookbook', RemoveDBToCookbookView.as_view(), name='remove_db_cookbook'),
    path('recipe/<int:pk>/likes', ShowAllLikes.as_view(), name='user_likes'),    
]

