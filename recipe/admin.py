from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Account)
admin.site.register(DBRecipe)
admin.site.register(UserRecipe)
admin.site.register(Image)
admin.site.register(Friend)
admin.site.register(Like)
admin.site.register(Cookbook)


# rating/reviews
# sharing with friends?
# "cookbooks"


