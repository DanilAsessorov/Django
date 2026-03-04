import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from catalog.services import get_products_by_category, get_product_detail, clear_products_cache
from catalog.models import Category

print("=" * 60)
print("ТЕСТИРОВАНИЕ СЕРВИСНЫХ ФУНКЦИЙ")
print("=" * 60)

# Тест 1: Получение всех продуктов
print("\n1. Получение всех продуктов:")
products = get_products_by_category()
print(f"   Найдено продуктов: {len(products)}")
for p in products[:3]:  # Покажем первые 3
    print(f"   - {p.name} ({p.price} руб.)")

# Тест 2: Получение продуктов по категории
print("\n2. Получение продуктов по категории:")
categories = Category.objects.all()
if categories:
    cat = categories[0]
    print(f"   Категория: {cat.name}")
    products = get_products_by_category(cat.id)
    print(f"   Найдено продуктов: {len(products)}")
    for p in products[:3]:
        print(f"   - {p.name}")

# Тест 3: Детальная информация о продукте
print("\n3. Детальная информация о продукте:")
if products:
    product_id = products[0].id
    product = get_product_detail(product_id)
    print(f"   Продукт: {product.name}")
    print(f"   Цена: {product.price}")
    print(f"   Категория: {product.category.name if product.category else 'Нет'}")

# Тест 4: Очистка кеша
print("\n4. Очистка кеша:")
clear_products_cache()
print("   Кеш очищен")

print("\n" + "=" * 60)
print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
print("=" * 60)