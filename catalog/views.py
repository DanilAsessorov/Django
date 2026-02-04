from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
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
    """Контроллер для страницы детального просмотра товара (CBV)"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


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
    """Создание нового продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование продукта"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """Удаление продукта"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление продукта: {self.object.name}'
        return context