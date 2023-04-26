from django.shortcuts import render

menu = [{'title': "Home", 'url_name': 'home_page_path'},
        # {'title': "Add new task", 'url_name': 'add_task_path'},
        # {'title': "Add category", 'url_name': 'add_category'},
        # {'title': "Войти", 'url_name': 'login'}
        ]

# Create your views here.


def main_page(request):
    pass
    context = {'menu':menu}
    return render(request, 'todo/add_task.html', context)
