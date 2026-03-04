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
cache.set('test_key', 'Hello Redis!', timeout=30)
print("   ✓ Данные записаны")

# Тест 2: Чтение
print("\n2. Попытка чтения из кеша...")
value = cache.get('test_key')
if value:
    print(f"   ✓ Данные прочитаны: '{value}'")
else:
    print("   ✗ Ошибка чтения!")

# Тест 3: Удаление
print("\n3. Попытка удаления...")
cache.delete('test_key')
value = cache.get('test_key')
print(f"   ✓ Ключ удален: {value is None}")

# Тест 4: Статистика (если доступно)
print("\n4. Проверка статистики...")
try:
    from django_redis import get_redis_connection
    conn = get_redis_connection("default")
    info = conn.info()
    print(f"   ✓ Redis version: {info.get('redis_version')}")
    print(f"   ✓ Connected clients: {info.get('connected_clients')}")
    print(f"   ✓ Used memory: {info.get('used_memory_human')}")
except:
    print("   ⚠ Статистика недоступна")

print("\n" + "=" * 60)
print("ЕСЛИ ВСЕ ТЕСТЫ ПРОШЛИ - REDIS РАБОТАЕТ! 🎉")
print("=" * 60)