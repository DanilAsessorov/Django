from django.core.management.base import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Создание тестовых данных"

    def handle(self, *args, **options):
        # Удаление старых данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий
        categories = [
            {"name": "Электроника", "description": "Гаджеты и устройства"},
            {"name": "Книги", "description": "Печатные издания"},
            {"name": "Одежда", "description": "Мужская и женская одежда"},
        ]

        created_categories = []
        for cat_data in categories:
            category = Category.objects.create(**cat_data)
            created_categories.append(category)
            self.stdout.write(f"Создана категория: {category.name}")

        # Создание продуктов
        products = [
            {
                "name": "Смартфон",
                "description": "Новый смартфон",
                "price": 29999.99,
                "category": created_categories[0]
            },
            {
                "name": "Ноутбук",
                "description": "Игровой ноутбук",
                "price": 89999.99,
                "category": created_categories[0]
            },
            {
                "name": "Роман",
                "description": "Художественная литература",
                "price": 599.99,
                "category": created_categories[1]
            },
        ]

        for prod_data in products:
            product = Product.objects.create(**prod_data)
            self.stdout.write(f"Создан продукт: {product.name}")

        self.stdout.write(
            self.style.SUCCESS("Тестовые данные успешно созданы!")
        )
