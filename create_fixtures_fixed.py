import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from catalog.models import Category, Product
from django.core.files import File

# Создание категорий
categories_data = [
    {'name': 'Электроника', 'description': 'Гаджеты и устройства'},
    {'name': 'Одежда', 'description': 'Модная одежда'},
    {'name': 'Книги', 'description': 'Литература разных жанров'},
    {'name': 'Спорт', 'description': 'Спортивные товары'},
]

# Очистка старых данных
Product.objects.all().delete()
Category.objects.all().delete()

categories = []
for cat_data in categories_data:
    category = Category.objects.create(**cat_data)
    categories.append(category)
    print(f"Создана категория: {category.name}")

# Создание продуктов
products_data = [
    {
        'name': 'Смартфон XYZ',
        'description': 'Мощный смартфон с отличной камерой',
        'price': 29999.99,
        'category': categories[0],
        'is_published': True,
    },
    {
        'name': 'Футболка Premium',
        'description': 'Качественная хлопковая футболка',
        'price': 1999.50,
        'category': categories[1],
        'is_published': True,
    },
    {
        'name': 'Книга по Django',
        'description': 'Подробное руководство по Django фреймворку',
        'price': 1500.00,
        'category': categories[2],
        'is_published': False,  # Не опубликована!
    },
    # ... добавьте больше продуктов
]

for prod_data in products_data:
    product = Product.objects.create(**prod_data)
    print(f"Создан продукт: {product.name} - {product.price} руб.")

    # Можно добавить логику для изображений если нужно
    # if some_condition:
    #     with open('path/to/image.jpg', 'rb') as f:
    #         product.image.save('image.jpg', File(f), save=True)

print(f"\nСоздано: {Category.objects.count()} категорий, {Product.objects.count()} продуктов")