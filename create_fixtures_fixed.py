import json

categories = [
    {
        "model": "catalog.category",
        "pk": 1,
        "fields": {
            "name": "Электроника",
            "description": "Техника и гаджеты"
        }
    },
    {
        "model": "catalog.category",
        "pk": 2,
        "fields": {
            "name": "Книги",
            "description": "Художественная литература"
        }
    },
    {
        "model": "catalog.category",
        "pk": 3,
        "fields": {
            "name": "Одежда",
            "description": "Модная одежда"
        }
    }
]

products = [
    {
        "model": "catalog.product",
        "pk": 1,
        "fields": {
            "name": "Смартфон Samsung Galaxy S23",
            "description": "Флагманский смартфон",
            "image": "products/smartphone.jpg",
            "category": 1,
            "price": "79999.99",
            "created_at": "2024-01-13T10:00:00Z",
            "updated_at": "2024-01-13T10:00:00Z"
        }
    },
    {
        "model": "catalog.product",
        "pk": 2,
        "fields": {
            "name": "Ноутбук ASUS ROG",
            "description": "Игровой ноутбук",
            "image": "products/laptop.jpg",
            "category": 1,
            "price": "129999.99",
            "created_at": "2024-01-13T10:00:00Z",
            "updated_at": "2024-01-13T10:00:00Z"
        }
    }
]

# Сохраняем с UTF-8
with open('catalog/fixtures/categories.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, indent=2, ensure_ascii=False)

with open('catalog/fixtures/products.json', 'w', encoding='utf-8') as f:
    json.dump(products, f, indent=2, ensure_ascii=False)

print("Фикстуры созданы в UTF-8")