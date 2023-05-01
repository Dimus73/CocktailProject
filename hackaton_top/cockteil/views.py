from django.shortcuts import render
from .models import *
from .forms import SetSearchForm, CocktailSerchNameForm, CocktailSerchIngradientForm
import requests
import json
import datetime
from cockteil.functions import cockteil_info

menu = [{'title': "Home", 'url_name': 'main_page_path'},
        {'title': "Ingredients", 'url_name': 'ingradients_list_path'},
        {'title': "Cocktails search", 'url_name': 'search_cocktail_path'},
        {'title': "Favorites", 'url_name': 'favorites_path'}
        ]


# Create your views here.
# *********************

def main_page(request):
    cock_list={'ks':[]}
    url_coct = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'
    param_coct = {'i':0}
    cocktail_recip=get_outside_request(url_coct, param_coct)
    cock = cockteil_info(cocktail_recip['drinks'][0])
    print (cock)
    cock_list['ks'].append(cock)
    day = datetime.date.today().strftime("%d-%m-%y")
    context = {'menu': menu, 'day':day, 'title':cock_list['ks'][0]['name'], "d_list":cock_list }
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
    title = "Ingredients list"
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

        transit={'cocktail_part_name':request_data.get('cocktail_part_name',False), 'ingradient':request_data.get('ingradient',False)}

        if request_data.get('cocktail_part_name',False):
            print ("***********Зашли в выбор названию")
            url = 'https://www.thecocktaildb.com/api/json/v1/1/search.php'
            param = {'s':request_data['cocktail_part_name']}
            f_n = CocktailSerchNameForm(request.POST)
            transit={'cocktail_part_name':request_data['cocktail_part_name'], 'ingradient':''}
        else:
            f_n = CocktailSerchNameForm()
            search_list=""
            # transit={}


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
            search_list=""
            # transit={}


        if request_data.get('add_to_base',False):
            print ("***********Зашли в добавление в базу")
            url_coct = 'https://www.thecocktaildb.com/api/json/v1/1/lookup.php'
            param_coct = {'i':int(request_data['add_to_base'])}
            coct_info=get_outside_request(url_coct, param_coct)
            try:
                FavoriteCocktails.objects.get(strDrink = coct_info['drinks'][0]['strDrink'])
                print("This cockteil in db. Adding interuption")
            except FavoriteCocktails.DoesNotExist:
                a = FavoriteCocktails(idDrink = coct_info['drinks'][0]['idDrink'],
                                    strDrink = coct_info['drinks'][0]['strDrink'] , 
                                    original_dict = json.dumps(coct_info['drinks'][0], indent=2))
                a.save()
                print("This cockteil added to db.")
                

        if request_data.get('clear_n',False) or request_data.get('clear_i',False):
            search_list=""
            transit={}
            f_n = CocktailSerchNameForm()
            f_i = CocktailSerchIngradientForm()
        else:
            if request_data.get('cocktail_part_name',False) or request_data.get('ingradient',False):
                search_list=get_outside_request(url, param)

    else:
        search_list=""
        transit={}
        f_n = CocktailSerchNameForm()
        f_i = CocktailSerchIngradientForm()

    title = "Cocktails search"

    f = {'f_n':f_n, 'f_i':f_i}
    context = {'menu': menu, 'title':title, 'search_list':search_list, 'form':f, 'transit':transit}
    return render(request, 'cockteil/search_cocktail.html', context)


def favorites(request):
    if request.method == 'POST':
        del_id = int(request.POST['button_id'])
        print (del_id)
        try:
            del_list = FavoriteCocktails.objects.filter(idDrink=del_id)
            for c in del_list:
                c.delete()
        except FavoriteCocktails.DoesNotExist:
            pass
    cock={}
    cock_list={'ks':[]}
    cock_data = FavoriteCocktails.objects.all()
    for k in cock_data:
        s_js= json.loads(k.original_dict)
        cock = cockteil_info (s_js)
        cock_list['ks'].append(cock)
    title = "Favorite cocktails"
    button_in_list=True
    context = {'menu': menu, 'title':title, 'd_list':cock_list, 'button_in_list':button_in_list}
    return render(request, 'cockteil/favorites.html', context)

def ingredient(request, idIngredient):
    a=Ingredients.objects.get(pk=idIngredient)
    context = {'menu': menu, 'title':a.name, "content": a}
    return render(request, 'cockteil/ingredient.html', context)

def cocktail(request, idDrink):
    cock_list={'ks':[]}
    url="https://www.thecocktaildb.com/api/json/v1/1/lookup.php"
    param = {'i':idDrink}
    cocktail_recip=get_outside_request(url, param)
    cock = cockteil_info(cocktail_recip['drinks'][0])
    cock_list['ks'].append(cock)
    context={'menu': menu, 'title':cock_list['ks'][0]['name'], "d_list": cock_list}
    return render(request, 'cockteil/cocktail.html', context)

def my_bar(request):
    if request.method == 'POST':
        form_info = request.POST
        print (form_info)
        bar = Ownbar.objects.all()
        for b in bar:
            v_key = 'v'+str(b.pk)
            c_key = 'c'+str(b.pk)
            if form_info.get(v_key,False):
                if b.quantity != int(form_info[v_key]):
                    print("Вносим", type(form_info[v_key]),form_info[v_key])
                    b.quantity = int(form_info[v_key])
                    b.save()
            if form_info.get(c_key,False):
                b.delete()
        # try:
        #     c = FavoriteCocktails.objects.get(idDrink=del_id)
        #     c.delete()
        # except FavoriteCocktails.DoesNotExist:
        #     pass

    bar = Ownbar.objects.all()
    # print (bar)

    title = "My bar"
    button_in_list=True
    context = {'menu': menu, 'title':title, 'bar':bar, 'button_in_list':button_in_list}
    return render(request, 'cockteil/bar.html', context)
