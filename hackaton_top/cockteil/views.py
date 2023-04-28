from django.shortcuts import render
from .models import *
from .forms import SetSearchForm
import requests
import json
import time

menu = [{'title': "Home", 'url_name': 'main_page_path'},
        {'title': "Ingradients", 'url_name': 'ingradients_list_path'},
        # {'title': "Add category", 'url_name': 'add_category'},
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
    title = "Ingradients list"
    ingr_list = Ingredients.objects.all()
    f=SetSearchForm()
    context = {'menu': menu, 'title':title, 'ingr_list':ingr_list, 'form':f}
    return render(request, 'cockteil/ingradients_list.html', context)
