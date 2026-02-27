from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Product, Category
from .forms import ProductForm


# Главная страница и контакты
class HomeView(TemplateView):
    """Контроллер для главной страницы (CBV)"""
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Дополнительные данные на главную
        context['products'] = Product.objects.filter(is_published=True)[:5]
        return context


class ContactsView(TemplateView):
    """Контроллер для страницы контактов (CBV)"""
    template_name = 'catalog/contacts.html'


# Детальная страница продукта
class ProductDetailView(DetailView):
    """Контроллер для страницы детального просмотра товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверка прав для отображения кнопок
        context['can_edit'] = self.request.user == self.object.owner
        context['can_delete'] = (self.request.user == self.object.owner or
                                 self.request.user.has_perm('catalog.can_unpublish_product'))
        return context


# CRUD операции для продуктов
class ProductListView(ListView):
    """Список всех опубликованных продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by('name')


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание нового продукта (только для авторизованных)"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        """При создании автоматически назначаем владельца"""
        form.instance.owner = self.request.user
        messages.success(self.request, 'Продукт успешно создан!')
        return super().form_valid(form)

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
        messages.success(self.request, 'Продукт успешно обновлен!')
        return super().form_valid(form)

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
        messages.success(self.request, 'Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление продукта: {self.object.name}'
        return context