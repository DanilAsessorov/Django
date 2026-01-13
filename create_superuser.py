import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Создаем суперпользователя
user = User.objects.create_superuser(
    username='admin',
    email='da_da_1914@list.ru',
    password='Admin123!'  # Пароль на английской раскладке
)

print('Суперпользователь создан!')