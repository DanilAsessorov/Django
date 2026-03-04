from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.http import Http404
from .models import Product, Category
from .forms import ProductForm
from .services import get_product_detail, get_products_by_category, clear_products_cache, clear_product_detail_cache


# Главная страница и контакты
class HomeView(TemplateView):
    """Контроллер для главной страницы (CBV)"""
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Кеширование списка продуктов на главной
        cache_key = 'home_products'
        products = cache.get(cache_key)

        if products is None:
            products = list(Product.objects.filter(is_published=True)[:5])
            cache.set(cache_key, products, timeout=300)  # 5 минут

        context['products'] = products
        context['categories'] = Category.objects.all()
        return context


class ContactsView(TemplateView):
    """Контроллер для страницы контактов (CBV)"""
    template_name = 'catalog/contacts.html'


# Кеширование детальной страницы продукта (5 минут)
@method_decorator(cache_page(300), name='dispatch')
class ProductDetailView(DetailView):
    """Контроллер для страницы детального просмотра товара (с кешированием)"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        # Используем сервисную функцию с кешированием
        product_id = self.kwargs.get(self.pk_url_kwarg)
        product = get_product_detail(product_id)

        if product is None:
            raise Http404("Продукт не найден")

        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверка прав для отображения кнопок
        context['can_edit'] = self.request.user == self.object.owner
        context['can_delete'] = (self.request.user == self.object.owner or
                                 self.request.user.has_perm('catalog.can_unpublish_product'))
        return context


class ProductByCategoryView(ListView):
    """Список продуктов в указанной категории (с кешированием)"""
    model = Product
    template_name = 'catalog/product_by_category.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        # Используем сервисную функцию с кешированием
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')

        # Получаем информацию о категории
        try:
            category = Category.objects.get(id=category_id)
            context['category'] = category
            context['title'] = f'Товары в категории: {category.name}'
        except Category.DoesNotExist:
            context['title'] = 'Все товары'

        # Список всех категорий для навигации
        context['categories'] = Category.objects.all()

        return context


class ProductListView(ListView):
    """Список всех опубликованных продуктов (с низкоуровневым кешированием)"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        # Пытаемся получить из кеша
        cache_key = 'all_products_list'
        products = cache.get(cache_key)

        if products is None:
            products = list(Product.objects.filter(
                is_published=True
            ).select_related('category', 'owner').order_by('name'))
            cache.set(cache_key, products, timeout=600)  # 10 минут
            print("[CACHE MISS] Список продуктов загружен из БД")
        else:
            print("[CACHE HIT] Список продуктов загружен из кеша")

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        """При создании автоматически назначаем владельца"""
        form.instance.owner = self.request.user
        response = super().form_valid(form)

        # Очищаем кеш
        clear_products_cache()
        cache.delete('all_products_list')
        cache.delete('home_products')

        messages.success(self.request, 'Продукт успешно создан!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title'] = 'Создание продукта'
        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование продукта (только владелец)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        """Проверка прав на редактирование"""
        product = self.get_object()
        return self.request.user == product.owner

    def handle_no_permission(self):
        """Если нет прав"""
        messages.error(self.request, 'У вас нет прав для редактирования этого продукта')
        raise PermissionDenied("У вас нет прав для редактирования этого продукта")

    def form_valid(self, form):
        response = super().form_valid(form)

        # Очищаем кеш
        clear_products_cache(self.object.category_id)
        cache.delete('all_products_list')
        cache.delete('home_products')
        clear_product_detail_cache(self.object.id)

        messages.success(self.request, 'Продукт успешно обновлен!')
        return response

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title'] = f'Редактирование: {self.object.name}'
        return context


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Удаление продукта (владелец или модератор)"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        """Проверка прав на удаление"""
        product = self.get_object()
        # Владелец ИЛИ модератор с правом can_unpublish_product
        return (self.request.user == product.owner or
                self.request.user.has_perm('catalog.can_unpublish_product'))

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для удаления этого продукта')
        raise PermissionDenied("У вас нет прав для удаления этого продукта")

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        category_id = product.category_id
        product_id = product.id
        response = super().delete(request, *args, **kwargs)

        # Очищаем кеш
        clear_products_cache(category_id)
        cache.delete('all_products_list')
        cache.delete('home_products')
        clear_product_detail_cache(product_id)

        messages.success(self.request, 'Продукт успешно удален!')
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление продукта: {self.object.name}'
        return context