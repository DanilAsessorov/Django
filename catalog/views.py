from django.shortcuts import render

def home(request):
    """контроллер для главной страницы"""
    return render(request, 'catalog/home.html')

def contacts(request):
    """контроллер для страницы контактов"""
    return render(request, 'catalog/contacts.html')
