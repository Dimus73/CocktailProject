from django.shortcuts import render
from .models import *
from .forms import SetSearchForm, CocktailSerchNameForm, CocktailSerchIngradientForm
import requests
import json
import time

menu = [{'title': "Home", 'url_name': 'main_page_path'},
        {'title': "Ingradients", 'url_name': 'ingradients_list_path'},
        {'title': "Cocktail search", 'url_name': 'search_cocktail_path'},
        # {'title': "Войти", 'url_name': 'login'}
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



def search_cocktail(request):
    title = "Search page"
    search_list=[]
    f_n = CocktailSerchNameForm()
    f_i = CocktailSerchIngradientForm()
    f = {'f_n':f_n, 'f_i':f_i}
    transit={}
    context = {'menu': menu, 'title':title, 'search_list':search_list, 'form':f, 'transit':transit}
    return render(request, 'cockteil/search_cocktail.html', context)
