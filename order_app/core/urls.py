# core/urls.py

from django.urls import path

from .views import OrderCreateView, OrderDeleteView, OrderDetailView, OrderUpdateView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductUpdateView, UserCreateView,CustomerCreateView, CustomerDeleteView, CustomerDetailView, CustomerListView, CustomerUpdateView, OrderListView, ProductListView, VendorDeleteView, VendorDetailView, VendorListView, VendorUpdateView
from .views import VendorCreateView, CustomerDeleteView, CustomerDetailView, CustomerListView, CustomerUpdateView

urlpatterns = [
    path('customers/', CustomerListView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/create/', CustomerCreateView.as_view(), name='customer-create'),
    path('customers/<int:pk>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('customers/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('vendors/create/', VendorCreateView.as_view(), name='vendor-create'),
    path('vendors/<int:pk>/update/', VendorUpdateView.as_view(), name='vendor-update'),
    path('vendors/<int:pk>/delete/', VendorDeleteView.as_view(), name='vendor-delete'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/create/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='order-update'),
    path('orders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    # Add URLs for products and orders similarly
]
