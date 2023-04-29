from django.contrib import admin
from .models import IngredientsType, Ingredients, Recipe

admin.site.register(IngredientsType)
admin.site.register(Ingredients)
admin.site.register(Recipe)

