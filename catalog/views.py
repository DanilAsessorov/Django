from django.views.generic import DetailView
from .models import Product
from django.views.generic import TemplateView

class HomeView(TemplateView):
    """Контроллер для главной страницы (CBV)"""
    template_name = 'catalog/home.html'


class ContactsView(TemplateView):
    """Контроллер для страницы контактов (CBV)"""
    template_name = 'catalog/contacts.html'


class ProductDetailView(DetailView):
    """Контроллер для страницы детального просмотра товара (CBV)"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        """Метод для передачи дополнительных данных в шаблон"""
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(category=self.object.category).exclude(id=self.object.id)[:4]
        return context