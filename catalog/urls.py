from django.urls import path
from .views import (
    HomeView,
    ContactsView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductListView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),

    # CRUD для продуктов
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]