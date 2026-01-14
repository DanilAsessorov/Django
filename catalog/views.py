from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    """Контроллер для страницы одного товара"""
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
        'title': product.name
    }
    return render(request, 'catalog/product_detail.html', context)

def home(request):
    """Контроллер для главной страницы"""
    products = Product.objects.all()[:6]  # Показываем первые 6 товаров
    context = {
        'products': products,
        'title': 'Главная страница'
    }
    return render(request, 'catalog/home.html', context)

def contacts(request):
    """контроллер для страницы контактов"""
    return render(request, 'catalog/contacts.html')
