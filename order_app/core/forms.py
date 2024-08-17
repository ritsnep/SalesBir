from django import forms
from .models import Customer, Vendor, Product, Category
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Company
from .models import Order, OrderItem

class CustomUserCreationForm(UserCreationForm):
    company = forms.ModelChoiceField(queryset=Company.objects.all(), required=False)

    class Meta:
        model = User
        fields = ('username', 'role', 'company', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        company = cleaned_data.get("company")

        if role == 'company_user' and not company:
            raise forms.ValidationError("Company User must be associated with a company.")

        return cleaned_data

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address']  # Exclude the 'company' field
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }
class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description','category', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
        }

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

OrderItemFormSet = forms.inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=True)
