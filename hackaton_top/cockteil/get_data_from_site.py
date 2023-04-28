from django.shortcuts import render
import requests
import json
import time

menu = [{'title': "Home", 'url_name': 'main_page_path'},
        # {'title': "Add new task", 'url_name': 'add_task_path'},
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
    all_ingr = {'ingredients': []}


    context = {'menu': menu}
    return render(request, 'cockteil/main_page.html', context)
