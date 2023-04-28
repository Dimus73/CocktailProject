from django.db import models

# Create your models here.
# class 

class IngredientsType (models.Model):
    name           = models.CharField (max_length=100, blank=False, db_index=True)

class Ingredients (models.Model):
    idIngredient   = models.IntegerField (blank = True, null=True)
    name           = models.CharField (max_length=100, blank=False, db_index=True)
    description    = models.TextField (blank=True, null=True)
    type           = models.ForeignKey (IngredientsType, on_delete=models.DO_NOTHING)
    alcohol        = models.BooleanField (default=False)
    abv            = models.IntegerField (default=0)

class ownbar (models.Model):
    ingradient     = models.ForeignKey(Ingredients, on_delete=models.DO_NOTHING)
    quantity       = models.IntegerField (default=0)



    