import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from django.conf import settings
from catalog.models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 50)
print("ФИНАЛЬНАЯ ПРОВЕРКА ПРОЕКТА")
print("=" * 50)

# 1. Проверка настроек
print("\n1. НАСТРОЙКИ БАЗЫ ДАННЫХ:")
db = settings.DATABASES['default']
print(f"   Движок: {db['ENGINE']}")
print(f"   Имя БД: {db['NAME']}")
print(f"   Пользователь: {db['USER']}")

# 2. Проверка моделей
print("\n2. ПРОВЕРКА МОДЕЛЕЙ:")
print(f"   Категорий в базе: {Category.objects.count()}")
print(f"   Продуктов в базе: {Product.objects.count()}")

# 3. Проверка суперпользователя
print("\n3. СУПЕРПОЛЬЗОВАТЕЛЬ:")
superusers = User.objects.filter(is_superuser=True)
if superusers.exists():
    print(f"   ✅ Есть суперпользователь: {superusers.first().username}")
else:
    print("   ❌ Нет суперпользователя!")

# 4. Проверка данных
print("\n4. ДАННЫЕ В БАЗЕ:")
if Category.objects.exists():
    print("   Категории:")
    for cat in Category.objects.all()[:3]:
        print(f"     - {cat.name}")
if Product.objects.exists():
    print("   Продукты:")
    for prod in Product.objects.all()[:3]:
        print(f"     - {prod.name} ({prod.price} руб.)")

# 5. Проверка настроек
print("\n5. ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ:")
print(f"   DEBUG режим: {settings.DEBUG}")
print(f"   MEDIA URL: {settings.MEDIA_URL}")
print(f"   STATIC URL: {settings.STATIC_URL}")

print("\n" + "=" * 50)
print("ПРОВЕРКА ЗАВЕРШЕНА!")
print("=" * 50)