import os
import django
import random
import datetime
import json
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaton.settings')
django.setup()

from cockteil.models import *

# cat_list=IngredientsType.objects.all()
# out={'pict':[]}
# for p in cat_list:
#     out['pict'].append({'pk':p.pk, 'url_str':p.image_url})
# print (out)

with open('bbbase.json','r') as f:
    info=json.load(f)

print(info)

for p in info['pict']:
    r=IngredientsType.objects.get(name=p['name'])
    r.image_url = p['url_str']
    r.save()