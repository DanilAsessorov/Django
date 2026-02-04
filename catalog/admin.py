from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_published', 'price')
    actions = ['make_published', 'make_unpublished']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)

    make_published.short_description = "Опубликовать выбранные продукты"

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)

    make_unpublished.short_description = "Снять с публикации выбранные продукты"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)