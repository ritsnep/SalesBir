# core/views.py

import logging
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect,render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Customer, Vendor, Product, Order,Category
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .forms import CustomerForm, OrderForm, OrderItemFormSet, VendorForm, ProductForm, ProductCategoryForm

# Customer Views
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from .models import User
from .forms import CustomUserCreationForm
import logging

logger = logging.getLogger(__name__)
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = AuthenticationForm

    def form_invalid(self, form):
        # If the form is invalid (e.g., wrong username or password), it will display an error message.
        return self.render_to_response(self.get_context_data(form=form))
    
class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/user_form.html'
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            form.add_error(None, e)
            return self.form_invalid(form)

class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Customer
    template_name = 'core/customer_list.html'
    permission_required = 'core.view_customer'

    def get_queryset(self):
        return Customer.objects.filter(company=self.request.user.company)

class VendorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Vendor
    template_name = 'core/vendor_list.html'
    permission_required = 'core.view_vendor'

    def get_queryset(self):
        return Vendor.objects.filter(company=self.request.user.company)

# Similar views for Product and Order can be created

class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    template_name = 'core/product_list.html'
    permission_required = 'core.view_product'

    def get_queryset(self):
        return Product.objects.filter(company=self.request.user.company)

# Similar views for Product and Order can be created

# class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
#     model = Order
#     template_name = 'core/order_list.html'
#     permission_required = 'core.view_order'

#     def get_queryset(self):
#         return Order.objects.filter(company=self.request.user.company)


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        return redirect('/') 
    

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'core/customer_detail.html'

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'core/customer_form.html'
    success_url = '/core/customers/'

    def form_valid(self, form):
        company = self.request.user.company
        if company is None:
            return HttpResponseBadRequest("User is not associated with any company.")
        form.instance.company = company
        logging.info(f"Customer will be associated with company: {company}")
        return super().form_valid(form)

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'core/customer_form.html'
    success_url = reverse_lazy('customer-list')

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'core/customer_confirm_delete.html'
    success_url = reverse_lazy('customer-list')

# Vendor Views

class VendorDetailView(DetailView):
    model = Vendor
    template_name = 'core/vendor_detail.html'

class VendorCreateView(LoginRequiredMixin, CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'core/vendor_form.html'
    success_url = '/core/vendors/'

    def form_valid(self, form):
        company = self.request.user.company
        if company is None:
            return HttpResponseBadRequest("User is not associated with any company.")
        form.instance.company = company
        logging.info(f"Vendor will be associated with company: {company}")
        return super().form_valid(form)

class VendorUpdateView(UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'core/vendor_form.html'
    success_url = reverse_lazy('vendor-list')

class VendorDeleteView(DeleteView):
    model = Vendor
    template_name = 'core/Vendor_confirm_delete.html'
    success_url = reverse_lazy('vendor-list')

# Product Views

class ProductDetailView(DetailView):
    model = Product
    template_name = 'core/product_detail.html'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'core/product_form.html'
    success_url = '/core/products/'

    def form_valid(self, form):
        company = self.request.user.company
        if company is None:
            return HttpResponseBadRequest("User is not associated with any company.")
        form.instance.company = company
        logging.info(f"Product will be associated with company: {company}")
        return super().form_valid(form)

class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'core/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'core/Product_confirm_delete.html'
    success_url = reverse_lazy('product-list')
# Product Category Views
class ProductCategoryListView(ListView):
    model = Category
    template_name = 'core/product_category_list.html'

class ProductCategoryCreateView(CreateView):
    model = Category
    form_class = ProductCategoryForm
    template_name = 'core/product_category_form.html'

# class OrderListView(ListView):
#     model = Order
#     template_name = 'core/order_list.html'
#     context_object_name = 'orders'
    
#     def get_queryset(self):
#         return Vendor.objects.filter(company=self.request.user.company)
class OrderListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'core/order_list.html'
    permission_required = 'core.view_order'

    def get_queryset(self):
        return Order.objects.filter(company=self.request.user.company)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'core/order_detail.html'
    context_object_name = 'order'

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'core/order_form.html'
    success_url = reverse_lazy('order-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = OrderItemFormSet(self.request.POST)
        else:
            data['items'] = OrderItemFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        form.instance.company = self.request.user.company
        if form.is_valid() and items.is_valid():
            self.object = form.save()
            items.instance = self.object
            items.save()
            self.object.calculate_total_amount()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'core/order_form.html'
    success_url = reverse_lazy('order-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            data['items'] = OrderItemFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        if form.is_valid() and items.is_valid():
            self.object = form.save()
            items.instance = self.object
            items.save()
            self.object.calculate_total_amount()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)
        


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'core/order_confirm_delete.html'
    success_url = reverse_lazy('order-list')