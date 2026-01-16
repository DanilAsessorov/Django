from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Контроллер для главной страницы (CBV)"""
    template_name = 'catalog/home.html'


class ContactsView(TemplateView):
    """Контроллер для страницы контактов (CBV)"""
    template_name = 'catalog/contacts.html'
