from django.core.cache import cache
from .models import Product, Category


def get_products_by_category(category_id=None):
    """
    Возвращает список продуктов в указанной категории
    с использованием кеширования
    """
    # Формируем ключ для кеша
    if category_id:
        cache_key = f'products_category_{category_id}'
    else:
        cache_key = 'products_all'

    # Пытаемся получить данные из кеша
    products = cache.get(cache_key)

    if products is None:
        # Если данных нет в кеше - получаем из БД
        queryset = Product.objects.filter(is_published=True).select_related('category', 'owner')

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        products = list(queryset.order_by('name'))  # Преобразуем в список для кеширования

        # Сохраняем в кеш на 15 минут (900 секунд)
        cache.set(cache_key, products, timeout=900)
        print(f"[CACHE MISS] Данные для {cache_key} загружены из БД")
    else:
        print(f"[CACHE HIT] Данные для {cache_key} загружены из кеша")

    return products


def get_product_detail(product_id):
    """
    Получение детальной информации о продукте с кешированием
    """
    cache_key = f'product_detail_{product_id}'
    product = cache.get(cache_key)

    if product is None:
        try:
            product = Product.objects.select_related('category', 'owner').get(id=product_id, is_published=True)
            cache.set(cache_key, product, timeout=300)  # 5 минут
            print(f"[CACHE MISS] Продукт {product_id} загружен из БД")
        except Product.DoesNotExist:
            return None
    else:
        print(f"[CACHE HIT] Продукт {product_id} загружен из кеша")

    return product


def clear_products_cache(category_id=None):
    """Очистка кеша продуктов"""
    if category_id:
        cache.delete(f'products_category_{category_id}')
        print(f"[CACHE CLEAR] Кеш для категории {category_id} очищен")
    else:
        # Очищаем кеш всех категорий
        cache.delete('products_all')
        cache.delete_pattern('products_category_*')  # Очищаем все категории по паттерну
        print(f"[CACHE CLEAR] Кеш всех продуктов очищен")


def clear_product_detail_cache(product_id):
    """Очистка кеша конкретного продукта"""
    cache_key = f'product_detail_{product_id}'
    cache.delete(cache_key)
    print(f"[CACHE CLEAR] Кеш продукта {product_id} очищен")