#!/usr/bin/env python
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'online_store.settings')
django.setup()

from catalog.forms import ProductForm, FORBIDDEN_WORDS


def run_tests():
    print("=" * 60)
    print("ТЕСТИРОВАНИЕ ВАЛИДАЦИИ ФОРМЫ ПРОДУКТА")
    print("=" * 60)

    passed = 0
    total = 0

    # Тест 1: Запрещенные слова в названии
    total += 1
    print(f"\n{'=' * 40}")
    print("ТЕСТ 1: Запрещенные слова в названии")
    print(f"{'=' * 40}")
    form_data = {
        'name': 'Лучшее казино в городе',
        'description': 'Отличный продукт',
        'price': 100,
        'is_published': True,
    }
    form = ProductForm(data=form_data)
    if not form.is_valid() and 'name' in form.errors:
        print(f"✅ ПРОЙДЕН: Валидация названия сработала")
        print(f"   Ошибка: {form.errors['name'][0]}")
        passed += 1
    else:
        print(f"❌ ПРОВАЛЕН: Валидация не сработала для названия!")

    # Тест 2: Запрещенные слова в описании
    total += 1
    print(f"\n{'=' * 40}")
    print("ТЕСТ 2: Запрещенные слова в описании")
    print(f"{'=' * 40}")
    form_data = {
        'name': 'Нормальный продукт',
        'description': 'Купите криптовалюту выгодно! Дешево и бесплатно!',
        'price': 200,
        'is_published': True,
    }
    form = ProductForm(data=form_data)
    if not form.is_valid() and 'description' in form.errors:
        print(f"✅ ПРОЙДЕН: Валидация описания сработала")
        print(f"   Ошибка: {form.errors['description'][0]}")
        passed += 1
    else:
        print(f"❌ ПРОВАЛЕН: Валидация не сработала для описания!")
        print(f"   Ошибки формы: {form.errors if form.errors else 'Нет ошибок'}")

    # Тест 3: Множественные запрещенные слова
    total += 1
    print(f"\n{'=' * 40}")
    print("ТЕСТ 3: Несколько запрещенных слов")
    print(f"{'=' * 40}")
    form_data = {
        'name': 'Игра в казино',
        'description': 'Обман и полиция были рядом с биржей криптовалюты',
        'price': 300,
        'is_published': True,
    }
    form = ProductForm(data=form_data)
    if not form.is_valid():
        errors = []
        if 'name' in form.errors:
            errors.append(f"Название: {form.errors['name'][0]}")
        if 'description' in form.errors:
            errors.append(f"Описание: {form.errors['description'][0]}")

        if errors:
            print(f"✅ ПРОЙДЕН: Обнаружены {len(errors)} ошибки:")
            for error in errors:
                print(f"   - {error}")
            passed += 1
    else:
        print(f"❌ ПРОВАЛЕН: Валидация не сработала!")

    # Тест 4: Отрицательная цена
    total += 1
    print(f"\n{'=' * 40}")
    print("ТЕСТ 4: Отрицательная цена")
    print(f"{'=' * 40}")
    form_data = {
        'name': 'Хороший продукт',
        'description': 'Отличное качество',
        'price': -50,
        'is_published': True,
    }
    form = ProductForm(data=form_data)
    if not form.is_valid() and 'price' in form.errors:
        print(f"✅ ПРОЙДЕН: Валидация цены сработала")
        print(f"   Ошибка: {form.errors['price'][0]}")
        passed += 1
    else:
        print(f"❌ ПРОВАЛЕН: Валидация не сработала для цены!")

    # Тест 5: Цена равна нулю (допустимо)
    total += 1
    print(f"\n{'=' * 40}")
    print("ТЕСТ 5: Цена равна нулю (допустимо)")
    print(f"{'=' * 40}")
    form_data = {
        'name': 'Бесплатный продукт',
        'description': 'Отличное предложение',
        'price': 0,
        'is_published': True,
    }
    form = ProductForm(data=form_data)
    if form.is_valid():
        print(f"✅ ПРОЙДЕН: Цена 0 допустима")
        print(f"   Название: {form.cleaned_data['name']}")
        print(f"   Цена: {form.cleaned_data['price']}")
        passed += 1
    else:
        print(f"❌ ПРОВАЛЕН: Цена 0 не должна вызывать ошибку!")
        print(f"   Ошибки: {form.errors}")

    # Тест 6: Корректные данные (без запрещенных слов)
    total += 1
    print(f"\n{'=' * 40}")
    print("ТЕСТ 6: Корректные данные")
    print(f"{'=' * 40}")
    form_data = {
        'name': 'Качественный товар',
        'description': 'Отличное предложение по хорошей цене',
        'price': 1500,
        'is_published': True,
    }
    form = ProductForm(data=form_data)
    if form.is_valid():
        print(f"✅ ПРОЙДЕН: Форма валидна")
        print(f"   Название: {form.cleaned_data['name']}")
        print(f"   Цена: {form.cleaned_data['price']}")
        passed += 1
    else:
        print(f"❌ ПРОВАЛЕН: Корректные данные должны быть приняты!")
        print(f"   Ошибки: {form.errors}")

    # Тест 7: Проверка всех запрещенных слов
    total += 1
    print(f"\n{'=' * 40}")
    print("ТЕСТ 7: Проверка всех запрещенных слов")
    print(f"{'=' * 40}")

    test_words = FORBIDDEN_WORDS
    print(f"Всего запрещенных слов: {len(test_words)}")
    print("Список: " + ", ".join(test_words))

    failed_words = []
    for word in test_words:
        form_data = {
            'name': f'Продукт с {word}',
            'description': f'Описание содержит {word}',
            'price': 100,
            'is_published': True,
        }
        form = ProductForm(data=form_data)
        if form.is_valid():
            failed_words.append(word)

    if not failed_words:
        print(f"✅ ПРОЙДЕН: Все {len(test_words)} запрещенных слов обнаружены")
        passed += 1
    else:
        print(f"❌ ПРОВАЛЕН: Не обнаружены слова: {', '.join(failed_words)}")

    # Итоги
    print(f"\n{'=' * 60}")
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print(f"{'=' * 60}")
    print(f"Пройдено тестов: {passed}/{total}")
    print(f"Успешность: {passed / total * 100:.1f}%")

    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print(f"⚠️  Есть проблемы: {total - passed} тест(ов) не пройдено")

    return passed == total


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)