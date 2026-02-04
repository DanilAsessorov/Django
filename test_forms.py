#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from catalog.forms import ProductForm, FORBIDDEN_WORDS

# Тест 1: Запрещенные слова в названии
print("Тест 1: Запрещенные слова в названии")
form_data = {
    'name': 'Лучшее казино в городе',
    'description': 'Отличный продукт',
    'price': 100,
    'is_published': True,
}
form = ProductForm(data=form_data)
if not form.is_valid():
    print(f"✓ Валидация сработала: {form.errors['name']}")
else:
    print("✗ Валидация не сработала!")

# Тест 2:
print("\nТест 2: Запрещенные слова в описании")
form_data = {
    'name': 'Нормальный продукт',
    'description': 'Купите криптовалюту выгодно!',  # ← ЗАПРЕЩЕННОЕ СЛОВО
    'price': 200,
    'is_published': True,
}
form = ProductForm(data=form_data)
if not form.is_valid():
    print(f"✓ Валидация сработала: {form.errors.get('description', 'Нет ошибок')}")
else:
    print("✗ Валидация не сработала!")

# Тест 3: Отрицательная цена
print("\nТест 3: Отрицательная цена")
form_data = {
    'name': 'Хороший продукт',
    'description': 'Отличное качество',
    'price': -50,
    'is_published': True,
}
form = ProductForm(data=form_data)
if not form.is_valid():
    print(f"✓ Валидация сработала: {form.errors['price']}")
else:
    print("✗ Валидация не сработала!")

# Тест 4: Корректные данные
print("\nТест 4: Корректные данные")
form_data = {
    'name': 'Качественный товар',
    'description': 'Отличное предложение',
    'price': 1500,
    'is_published': True,
}
form = ProductForm(data=form_data)
if form.is_valid():
    print("✓ Форма валидна")
    print(f"  Название: {form.cleaned_data['name']}")
    print(f"  Цена: {form.cleaned_data['price']}")
else:
    print(f"✗ Ошибки: {form.errors}")