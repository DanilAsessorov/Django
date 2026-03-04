import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from django.core.cache import cache

print("=" * 60)
print("ПРОВЕРКА ПОДКЛЮЧЕНИЯ К REDIS")
print("=" * 60)

# Тест 1: Запись
print("\n1. Попытка записи в кеш...")
try:
    cache.set('test_key', 'Hello Redis!', timeout=30)
    print("   ✓ Данные записаны")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")

# Тест 2: Чтение
print("\n2. Попытка чтения из кеша...")
try:
    value = cache.get('test_key')
    if value:
        print(f"   ✓ Данные прочитаны: '{value}'")
    else:
        print("   ✗ Ошибка чтения!")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")

# Тест 3: Удаление
print("\n3. Попытка удаления...")
try:
    cache.delete('test_key')
    value = cache.get('test_key')
    print(f"   ✓ Ключ удален: {value is None}")
except Exception as e:
    print(f"   ✗ Ошибка: {e}")

# Тест 4: Простая проверка Redis через прямой connection
print("\n4. Прямая проверка Redis connection...")
try:
    import redis

    r = redis.Redis(host='localhost', port=6379, db=1)
    r.ping()
    print("   ✓ Redis сервер отвечает на ping")

    # Информация о сервере
    info = r.info()
    print(f"   ✓ Redis версия: {info.get('redis_version')}")
    print(f"   ✓ Запущен: {info.get('uptime_in_seconds')} сек")
except Exception as e:
    print(f"   ✗ Ошибка подключения к Redis: {e}")

print("\n" + "=" * 60)
print("ЕСЛИ ВСЕ ТЕСТЫ ПРОШЛИ - REDIS РАБОТАЕТ! 🎉")
print("=" * 60)