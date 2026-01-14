import os

# Создаем папки если их нет
os.makedirs("catalog/management/commands", exist_ok=True)

# Создаем __init__.py файлы
open("catalog/management/__init__.py", "w").close()
open("catalog/management/commands/__init__.py", "w").close()

# Содержимое команды
content = '''from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = "Создание тестовых данных"

    def handle(self, *args, **options):
        # Удаление старых данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий
        cat1 = Category.objects.create(name="Электроника", description="Гаджеты")
        cat2 = Category.objects.create(name="Книги", description="Литература")

        # Создание продуктов
        Product.objects.create(
            name="Смартфон",
            description="Мощный смартфон",
            price=29999.99,
            category=cat1
        )

        Product.objects.create(
            name="Ноутбук",
            description="Игровой ноутбук",
            price=89999.99,
            category=cat1
        )

        self.stdout.write("Тестовые данные созданы!")'''

# Сохраняем файл
with open("catalog/management/commands/fill_test_data.py", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Файл fill_test_data.py создан")
print("✅ Кодировка: UTF-8")