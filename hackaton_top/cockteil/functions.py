def cockteil_info (cocktail_recipe):
    
    cock_list={}
    cock_list['idDrink']      = cocktail_recipe['idDrink']
    cock_list['name']         = cocktail_recipe['strDrink']
    cock_list['type']         = cocktail_recipe['strCategory']
    cock_list['alcohol']      = cocktail_recipe['strAlcoholic']
    cock_list['glass']        = cocktail_recipe['strGlass']
    cock_list['instructions'] = cocktail_recipe['strInstructions']
    cock_list['image']        = cocktail_recipe['strDrinkThumb']
    cock_list['ingradient']   = {}
    for a in range(1,16):
        key= 'strIngredient' + str(a)
        value= 'strMeasure'  + str(a)
        if not cocktail_recipe[key] is None:
            cock_list['ingradient'][cocktail_recipe[key]]=cocktail_recipe[value]
    return(cock_list)


    
