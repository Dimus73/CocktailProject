from django.shortcuts import render
from .models import *
from .forms import SetSearchForm, CocktailSerchNameForm, CocktailSerchIngradientForm
import requests
import json
import time

menu = [{'title': "Home", 'url_name': 'main_page_path'},
        {'title': "Ingredients", 'url_name': 'ingradients_list_path'},
        {'title': "Cocktail search", 'url_name': 'search_cocktail_path'},
        {'title': "Favorites", 'url_name': 'favorites_path'}
        ]

url = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php'
param = {'iid': 552}


def get_outside_request(url, param):
    r = requests.get(url, param)
    if r.status_code == 200:
        content = r.content
        r.close()
        return (content)
    else:
        print(f'Parametr {param}. No ansver')
    r.close()


def get_and_save_external_data():

    for a in range(1, 1000):
        param['iid'] = a
        st = get_outside_request(url, param)
        try:
            s = json.loads(st)
            all_ingr['ingredients'].append(s['ingredients'][0])
        except TypeError:
            print(f'Похоже нет инградиента с номером {a}')
        print(s)
        time.sleep(2)

    with open("ingradients.json", 'w') as f:
        json.dump(all_ingr, f, indent=3)

# Create your views here.
# *********************


def main_page(request):
    context = {'menu': menu}
    return render(request, 'cockteil/main_page.html', context)

def ingradients_list(request):
    if request.method == 'POST':
        print(f'Пост запрос. будем отбирать\nПришло  IngradientName:{request.POST}')
        request_data = request.POST
        ingr_list = Ingredients.objects.all()
        if not 'my_button' in request_data:
            if 'button_id' in request_data:
                item=''
                try:
                    print("***********Ищем инградиент")
                    item=Ingredients.objects.get(pk=int(request_data['button_id']))
                except Ingredients.DoesNotExis:
                    pass 
                if item:
                    try:
                        print("**********Ищем в баре", item.pk)
                        v = Ownbar.objects.get(pk=item.pk)
                    except Ownbar.DoesNotExist:
                        b = Ownbar(ingradient=item, quantity=0)
                        b.save()
            if request_data['ingradient_name']:
                ingr_list = ingr_list.filter(name__icontains=request_data['ingradient_name'])
            if request_data['categories']:
                ingr_list = ingr_list.filter(type=request_data['categories'])
            if request_data.get('only_bar','False') != 'False':
                print("Показываем только в баре", type(request_data.get('only_bar',False)))
                bar_list = Ownbar.objects.all().values_list('ingradient')
                ingr_list = ingr_list.filter (pk__in=bar_list)
            transit={'ingradient_name':request_data['ingradient_name'], 'categories':request_data['categories'], 'only_bar':request_data.get('only_bar',False)}
            f = SetSearchForm(request.POST) 
        else:
            transit={'ingradient_name':'', 'categories':'', 'only_bar':False}
            f = SetSearchForm() 
    else:
       ingr_list = Ingredients.objects.all()
       f=SetSearchForm()
       transit={'ingradient_name':'', 'categories':'', 'only_bar':False}
    title = "Ingradients list"
    context = {'menu': menu, 'title':title, 'ingr_list':ingr_list, 'form':f, 'transit':transit}
    return render(request, 'cockteil/ingradients_list.html', context)

#Query Response Function
def get_outside_request(url, param):
    r = requests.get(url, param)
    if r.status_code == 200:
        content = json.loads(r.content)
        r.close()
        return (content)
    else:
        print(f'Parametr {param}. No ansver')
    r.close()


def search_cocktail(request):
    if request.method == 'POST':
        print(f'Пост запрос. будем отбирать\nПришло *****: {request.POST}')
        request_data = request.POST
        print (request_data)

        if request_data.get('cocktail_part_name',False):
            print ("***********Зашли в выбор названию")
            url = 'https://www.thecocktaildb.com/api/json/v1/1/search.php'
            param = {'s':request_data['cocktail_part_name']}
            f_n = CocktailSerchNameForm(request.POST)
            transit={'cocktail_part_name':request_data['cocktail_part_name'], 'ingradient':''}
        else:
            f_n = CocktailSerchNameForm()

        if request_data.get('ingradient',False):
            print ("***********Зашли в выбор инградиенту")
            try:
                ingadient = Ingredients.objects.get(pk=int(request_data['ingradient']))
                url = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php'
                param = {'i':ingadient}
                f_i = CocktailSerchIngradientForm(request.POST)
                transit={'cocktail_part_name':'', 'ingradient':request_data['ingradient']}
            except Ingredients.DoesNotExist:
                pass
        else:
            f_i = CocktailSerchIngradientForm()

        if request_data.get('add_to_base',False):
            print ("***********Зашли в добавление в базу")
            try:
                url_coct = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php'
                param_coct = {'i':int(request_data['add_to_base'])}
                coct_info=get_outside_request(url_coct, param_coct)
                print("**************** Запро конкретного коктеляё\n",coct_info)
                a = FavoriteCocktails(idDrink = coct_info['drinks'][0]['idDrink'],
                                      strDrink = coct_info['drinks'][0]['strDrink'] , 
                                      original_dict = json.dumps(coct_info['drinks'][0], indent=2))
                a.save()
            except FavoriteCocktails.DoesNotExist:
                print ("Не получилось записать в базу любымый коктель")
                

        if request_data.get('clear_n',False) or request_data.get('clear_i',False):
            search_list=""
            transit={}
            f_n = CocktailSerchNameForm()
            f_i = CocktailSerchIngradientForm()

        else:
            search_list=get_outside_request(url, param)
        print("***********Прошли ифы")

    else:
        search_list=""
        transit={}
        f_n = CocktailSerchNameForm()
        f_i = CocktailSerchIngradientForm()

            

    title = "Search cockteil page"

    f = {'f_n':f_n, 'f_i':f_i}
    context = {'menu': menu, 'title':title, 'search_list':search_list, 'form':f, 'transit':transit}
    return render(request, 'cockteil/search_cocktail.html', context)


def favorites(request):
    cock={}
    cock_list={'ks':[]}
    cock_data = FavoriteCocktails.objects.all()
    for k in cock_data:
        cock={}
        print ("*************\n",k.original_dict,"\n********************")
        s_js= json.loads(k.original_dict)
        cock['name']         = s_js['strDrink']
        cock['type']         = s_js['strCategory']
        cock['alcohol']      = s_js['strAlcoholic']
        cock['glass']        = s_js['strGlass']
        cock['instructions'] = s_js['strInstructions']
        cock['image']        = s_js['strDrinkThumb']
        cock['ingradient']   = {}
        for a in range(1,16):
            key= 'strIngredient' + str(a)
            value= 'strMeasure'  + str(a)
            if not s_js[key] is None:
                cock['ingradient'][s_js[key]]=s_js[value]
        cock_list['ks'].append(cock)
    
    for p in cock_list['ks']:
        print ("*************\n",p,"\n********************")

    print(cock_list)
    # print( cock_data[0].original_dict)
    # s=cock_data[0].original_dict
    # print(s)
    # s_js= json.loads(s)
    # print (type(s_js),s_js)
    # print( type( json.loads(cock_data[0].original_dict)))



    search_list=""
    transit={}
    title = "Favorits cockteil page"
    f = {}
    context = {'menu': menu, 'title':title, 'd_list':cock_list, 'form':f, 'transit':transit}
    return render(request, 'cockteil/favorites.html', context)


def ingredient(request, idIngredient):
    a=Ingredients.objects.get(pk=idIngredient)
    context = {'menu': menu, 'title':a.name, "content": a}
    return render(request, 'cockteil/ingredient.html', context)