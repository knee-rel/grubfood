from django.forms import ModelForm, HiddenInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer, Food, Order, OrderItem

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'description', 'price']
        placeholders = {
            "name": "Name",
            "description": "Description",
            "price": "Price"
        }
        
class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['firstname', 'lastname', 'address', 'city']
        
class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'paymentmode']

class OrderItemForm(ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'food', 'quantity']
        widgets = {
            'order': HiddenInput(),
        }

class CustomerOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'paymentmode']
        widgets = {
            'customer': HiddenInput(),
        }

# FOR THE LOGIN FORM
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
# class NewUserOrderForm(ModelForm):
#     class Meta:
#         model = Order
#         fields = ['food', 'quantity', 'paymentmode']