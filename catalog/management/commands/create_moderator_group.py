from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу модераторов с необходимыми правами'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('НАСТРОЙКА ГРУППЫ МОДЕРАТОРОВ'))
        self.stdout.write(self.style.SUCCESS('=' * 50))

        # Создаем группу
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Группа "Модератор продуктов" уже существует'))

        # Получаем content type для модели Product
        content_type = ContentType.objects.get_for_model(Product)

        # Получаем необходимые разрешения
        permissions = Permission.objects.filter(
            content_type=content_type,
            codename__in=['can_unpublish_product', 'delete_product']
        )

        # Добавляем разрешения группе
        for perm in permissions:
            moderator_group.permissions.add(perm)
            self.stdout.write(self.style.SUCCESS(f'  ✅ Добавлено право: {perm.name}'))

        # Проверяем результат
        group_perms = moderator_group.permissions.all()
        self.stdout.write(self.style.SUCCESS('-' * 50))
        self.stdout.write(self.style.SUCCESS(f'Итого прав у группы: {group_perms.count()}'))

        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('✅ Группа модераторов настроена успешно!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))