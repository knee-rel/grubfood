from django.contrib import admin
from .models import Customer, Food, Order, OrderItem

# Register your models here.
admin.site.register(Customer)
admin.site.register(Food)
admin.site.register(Order)
admin.site.register(OrderItem)