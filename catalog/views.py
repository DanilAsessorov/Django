from django.views.generic import TemplateView, DetailView, ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Product, Category
from .forms import ProductForm


# ============================================
# МИКСИНЫ ДЛЯ ПРОВЕРКИ ПРАВ
# ============================================

class ModeratorRequiredMixin(UserPassesTestMixin):
    """Проверка, что пользователь является модератором"""

    def test_func(self):
        return self.request.user.groups.filter(name='Модератор продуктов').exists() or self.request.user.is_superuser

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'У вас нет прав модератора для этого действия')
            return redirect('product_list')
        return super().handle_no_permission()


class OwnerOrModeratorMixin(UserPassesTestMixin):
    """Проверка, что пользователь - владелец или модератор"""

    def test_func(self):
        product = self.get_object()
        is_owner = product.owner == self.request.user
        is_moderator = self.request.user.groups.filter(
            name='Модератор продуктов').exists() or self.request.user.is_superuser
        return is_owner or is_moderator

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            messages.error(self.request, 'У вас нет прав для этого действия')
            return redirect('product_detail', pk=self.get_object().pk)
        return super().handle_no_permission()


# ============================================
# ПУБЛИЧНЫЕ СТРАНИЦЫ
# ============================================

class HomeView(TemplateView):
    """Контроллер для главной страницы"""
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(is_published=True)[:5]
        return context


class ContactsView(TemplateView):
    """Контроллер для страницы контактов"""
    template_name = 'catalog/contacts.html'


class ProductDetailView(DetailView):
    """Детальная страница продукта"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductListView(ListView):
    """Список всех опубликованных продуктов"""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.filter(is_published=True).order_by('name')


# ============================================
# CRUD ОПЕРАЦИИ (ТОЛЬКО ДЛЯ АВТОРИЗОВАННЫХ)
# ============================================

class ProductCreateView(LoginRequiredMixin, CreateView):
    """Создание продукта - доступно только авторизованным"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        # Автоматически назначаем владельца
        form.instance.owner = self.request.user
        messages.success(self.request, 'Продукт успешно создан!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductUpdateView(LoginRequiredMixin, OwnerOrModeratorMixin, UpdateView):
    """Редактирование продукта - только владелец"""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def get_success_url(self):
        messages.success(self.request, 'Продукт успешно обновлен!')
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDeleteView(LoginRequiredMixin, OwnerOrModeratorMixin, DeleteView):
    """Удаление продукта - только владелец или модератор"""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление продукта: {self.object.name}'
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Продукт успешно удален!')
        return super().delete(request, *args, **kwargs)


# ============================================
# ФУНКЦИЯ ДЛЯ ОТМЕНЫ ПУБЛИКАЦИИ (ТОЛЬКО МОДЕРАТОРЫ)
# ============================================

@login_required
@permission_required('catalog.can_unpublish_product', raise_exception=True)
def product_unpublish(request, pk):
    """Отмена публикации продукта (доступно только модераторам)"""
    product = get_object_or_404(Product, pk=pk)

    if product.is_published:
        product.is_published = False
        product.save()
        messages.success(request, f'Продукт "{product.name}" снят с публикации')
    else:
        messages.warning(request, f'Продукт "{product.name}" уже не опубликован')

    return redirect('product_detail', pk=pk)