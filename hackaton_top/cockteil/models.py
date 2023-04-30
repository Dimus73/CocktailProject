from django.db import models

# Create your models here.
# class 

class IngredientsType (models.Model):
    name           = models.CharField (max_length=100, blank=False, db_index=True)
    image_url      = models.URLField (blank=True, null=True)

    def __str__(self):
        return self.name


class Ingredients (models.Model):
    idIngredient   = models.IntegerField (blank = True, null=True)
    name           = models.CharField (max_length=100, blank=False, db_index=True)
    description    = models.TextField (blank=True, null=True)
    type           = models.ForeignKey (IngredientsType, on_delete=models.DO_NOTHING)
    alcohol        = models.BooleanField (default=False)
    abv            = models.IntegerField (default=0)

    def __str__(self):
        return self.name
    def is_alcohol(self):
        return 'alcoholic' if self.alcohol else 'non-alcoholic'
    def is_it_in_bar(self):
        try:
            Ownbar.objects.get(ingradient=self.pk)
            return True
        except Ownbar.DoesNotExist:
            return False


class Ownbar (models.Model):
    ingradient     = models.ForeignKey(Ingredients, on_delete=models.DO_NOTHING)
    quantity       = models.IntegerField (default=0)

    def __str__(self):
        return self.ingradient.name


class FavoriteCocktails(models.Model):
    idDrink                               =models.IntegerField (blank = True, null=True)
    strDrink                              =models.CharField (max_length=100, blank=True, null=True, db_index=True)
    original_dict                         =models.TextField()




    