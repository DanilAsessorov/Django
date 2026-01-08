INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'catalog',  # Добавляем наше приложение
]

# Внизу файла добавляем:
STATIC_URL = '/static/'

# Для разработки
STATICFILES_DIRS = [
    BASE_DIR / "static",
]