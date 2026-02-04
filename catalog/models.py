from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    image = models.ImageField(upload_to="products/", verbose_name="Изображение", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Категория", blank=True, null=True, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]
        # Добавляем permissions для более тонкого контроля
        permissions = [
            ("can_unpublish", "Может снимать с публикации"),
        ]

    def __str__(self):
        return f"{self.name} - {self.price}"
