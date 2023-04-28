import json

def get_categorys (file_name)->json:
    category_list=[]
    with open(file_name, 'r') as f:
        file_data=json.load(f)
    for p in file_data['ingredients']:
        if p['strType'] not in category_list:
            category_list.append(p['strType'])
    print(category_list)
    
get_categorys('ingradients copy 2.json')