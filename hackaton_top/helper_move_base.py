import os
import django
import random
import datetime
import json
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackaton.settings')
django.setup()

from cockteil.models import *

cat_list=IngredientsType.objects.all()
out={'pict':[]}
for p in cat_list:
    out['pict'].append({'pk':p.pk, 'url_str':p.image_url, 'name':p.name})
print (out)
with open('bbbase.json','w') as f:
    json.dump(out, f, indent=2)

