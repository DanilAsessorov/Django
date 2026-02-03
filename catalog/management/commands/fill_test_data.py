from django.core.management.base import BaseCommand
from catalog.models import Category, Product
import os

class Command(BaseCommand):
    help = "Создание тестовых данных с изображениями"

    def handle(self, *args, **options):
        # Удаление старых данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание папки для изображений
        os.makedirs("media/products", exist_ok=True)

        # Создание категорий
        cat1 = Category.objects.create(name="Электроника", description="Гаджеты")
        cat2 = Category.objects.create(name="Книги", description="Литература")
        cat3 = Category.objects.create(name="Одежда", description="Одежда")

        # Создаем тестовые файлы изображений
        for img in ["smartphone.jpg", "laptop.jpg", "book.jpg", "tshirt.jpg"]:
            path = f"media/products/{img}"
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write("test")

        # Создание продуктов с изображениями
        Product.objects.create(
            name="Смартфон",
            description="Мощный смартфон",
            price=29999.99,
            category=cat1,
            image="products/smartphone.jpg"
        )

        Product.objects.create(
            name="Ноутбук",
            description="Игровой ноутбук",
            price=89999.99,
            category=cat1,
            image="products/laptop.jpg"
        )

        Product.objects.create(
            name="Книга",
            description="Интересная книга",
            price=1500.00,
            category=cat2,
            image="products/book.jpg"
        )

        Product.objects.create(
            name="Футболка",
            description="Хлопковая футболка",
            price=1999.99,
            category=cat3,
            image="products/tshirt.jpg"
        )

        self.stdout.write("Тестовые данные с изображениями созданы!")