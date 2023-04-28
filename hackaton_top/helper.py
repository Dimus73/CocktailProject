import os
import django
import random
import datetime
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaton.settings')
django.setup()

from cockteil.models import *


def get_categorys (file_name)->json:
    category_list=[]
    with open(file_name, 'r') as f:
        file_data=json.load(f)
    for p in file_data['ingredients']:
        if p['strType'] not in category_list:
            category_list.append(p['strType'])
    return (category_list)

def found_by_category (file_name, cat_name)->json:
    ingad_list=[]
    with open(file_name, 'r') as f:
        file_data=json.load(f)
    for p in file_data['ingredients']:
        # if p['strType'] n== cat_name:
        if p['strType'] is None:
            ingad_list.append(p)
    return (ingad_list)

def get_ingradient(file_name):
    ingad_list=[]
    with open(file_name, 'r') as f:
        file_data=json.load(f)
    for p in file_data['ingredients']:
        p['strType'] = 'Others' if p['strType'] is None else p['strType']
        p['strAlcohol'] = True if p['strAlcohol'] == 'Yes' else False
        p['strABV'] = 0 if p['strABV'] is None else p['strABV']
        ingad_list.append(p)
    return (ingad_list)


# cat_list = get_categorys('help_utils/ingradients copy 2.json')
# for p in cat_list:
#     if p is not None:
#         print(len(p),f"**{p}**")
#         a = IngredientsType(name=p)
#         a.save()
    # print (a.name)

# ingr = found_by_category('help_utils/ingradients copy 2.json','dd')
# for s in ingr:
#     print(s)

ingr = get_ingradient('help_utils/ingradients copy 2.json')
print ('Закончили считывать')
for p in ingr:
    idIngredient    = p["idIngredient"]
    name            = p['strIngredient']
    description     = p['strDescription']
    try:
        type            = IngredientsType.objects.get(name=p['strType'])
    except IngredientsType.MultipleObjectsReturned:
        print (f"Ошибка в {p['strType']}")
    alcohol         = p['strAlcohol']
    abv             = p['strABV']
    a = Ingredients(idIngredient = idIngredient, name = name, description=description, type=type, alcohol = alcohol, abv=abv)
    a.save()
    print (idIngredient, name, description, type, alcohol, abv)