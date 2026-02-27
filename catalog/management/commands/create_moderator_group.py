from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создание групп и назначение прав для модераторов'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Начало создания групп...'))

        # Создание группы модераторов
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(self.style.SUCCESS('✓ Группа "Модератор продуктов" создана'))
        else:
            self.stdout.write('ℹ Группа "Модератор продуктов" уже существует')

        # Получение прав для продукта
        content_type = ContentType.objects.get_for_model(Product)

        # Право на отмену публикации (кастомное)
        can_unpublish, unpublish_created = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может отменять публикацию продукта',
            content_type=content_type,
        )

        if unpublish_created:
            self.stdout.write(self.style.SUCCESS('✓ Право "can_unpublish_product" создано'))
        else:
            self.stdout.write('ℹ Право "can_unpublish_product" уже существует')

        # Право на удаление продукта (стандартное)
        try:
            can_delete = Permission.objects.get(
                codename='delete_product',
                content_type=content_type,
            )
            self.stdout.write('ℹ Право "delete_product" найдено')
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('✗ Право "delete_product" не найдено!'))
            return

        # Назначение прав группе
        moderator_group.permissions.add(can_unpublish, can_delete)
        self.stdout.write(self.style.SUCCESS('✓ Права назначены группе модераторов'))

        # Проверка назначенных прав
        permissions = moderator_group.permissions.all()
        self.stdout.write(self.style.NOTICE('\nНазначенные права:'))
        for perm in permissions:
            self.stdout.write(f'  - {perm.name} ({perm.codename})')

        self.stdout.write(self.style.SUCCESS('\n✓ Группы успешно созданы и настроены!'))