# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import Permission
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
import logging


# Set up logging
logger = logging.getLogger(__name__)

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_email = models.EmailField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('company_user', 'Company User'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.role == 'company_user':
            if not self.company:
                raise ValidationError("Company User must be associated with a company.")
            self.is_staff = True  # Allow access to admin but limited permissions

        super().save(*args, **kwargs)

        if self.role == 'company_user':
            self.user_permissions.clear()
            permissions = Permission.objects.filter(
                content_type__app_label='core',
                codename__in=[
                    'add_customer', 'change_customer', 'delete_customer', 'view_customer',
                    'add_vendor', 'change_vendor', 'delete_vendor', 'view_vendor',
                    'add_product', 'change_product', 'delete_product', 'view_product',
                    'add_order', 'change_order', 'delete_order', 'view_order',
                ]
            )
            self.user_permissions.add(*permissions)

    def __str__(self):
        return f"{self.username} ({self.role})"

# class User(AbstractUser):
#     ROLE_CHOICES = [
#         ('admin', 'Admin'),
#         ('company_user', 'Company User'),
#     ]

#     role = models.CharField(max_length=20, choices=ROLE_CHOICES)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_set',  # Changed related_name
#         blank=True,
#         help_text=('The groups this user belongs to. '
#                    'A user will get all permissions granted to each of their groups.'),
#         verbose_name=('groups'),
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_set',  # Changed related_name
#         blank=True,
#         help_text=('Specific permissions for this user.'),
#         verbose_name=('user permissions'),
#     )

#     def __str__(self):
#         return f"{self.username} ({self.role})"


class Customer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


# core/models.py

class Vendor(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name
# core/models.py

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
# core/models.py

class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
# core/models.py

# class Order(models.Model):
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     date = models.DateTimeField(auto_now_add=True)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"Order #{self.id} - {self.customer.name}"
# # core/models.py

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     quantity = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return f"{self.quantity} x {self.product.name}"

class Order(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.name}"

    def calculate_total_amount(self):
        total = sum(item.price * item.quantity for item in self.items.all())
        self.total_amount = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total(self):
        return self.quantity * self.price