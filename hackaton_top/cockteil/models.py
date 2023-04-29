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


class Recipe(models.Model):
    idDrink = models.IntegerField()
    strDrink       = models.CharField (max_length=150, blank=False, db_index=True)
    idIngredient   = models.IntegerField (blank = True, null=True)
    strGlass       = models.CharField ()
    strInstructions = models.TextField()
    strDrinkThumb   = models.URLField()
    strIngredient1 = models.CharField ()
    strIngredient2 = models.CharField ()
    strIngredient3 = models.CharField ()
    strIngredient4 = models.CharField ()
    strIngredient5 = models.CharField ()
    strIngredient6 = models.CharField ()
    strIngredient7 = models.CharField ()
    strIngredient8 = models.CharField ()
    strMeasure1 = models.CharField ()
    strMeasure2 = models.CharField ()
    strMeasure3 = models.CharField ()
    strMeasure4 = models.CharField ()
    strMeasure5 = models.CharField ()
    strMeasure6 = models.CharField ()
    strMeasure7 = models.CharField ()
    strMeasure8 = models.CharField ()






    def __str__(self):
        return f'{self.strDrink } {self.strGlass} {self.strInstructions} {self.strDrinkThumb} {self.strIngredient1} {self.strIngredient2}'