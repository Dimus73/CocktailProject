import os
import django
import random
import datetime
import json
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaton.settings')
django.setup()

from cockteil.models import *


url = 'https://www.thecocktaildb.com/api/json/v1/1/filter.php'
# param = {'iid': 552}
param = {'i':'Vodka'}


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

ansver = get_outside_request(url, param)
print (ansver)
st = json.loads(ansver)
j_st=json.dumps(st,indent=2)
print (j_st)