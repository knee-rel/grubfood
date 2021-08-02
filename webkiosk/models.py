from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.id}: {self.firstname}, {self.lastname}, {self.address}, {self.city}'
    
class Food(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.id}: {self.name}, {self.description}, {self.price}'
    
    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    PAYMENT_MODE_CHOICES = [
        #tuples
        ('CH', 'Cash'),
        ('CD', 'Card'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) 
    orderdatetime = models.DateTimeField(auto_now_add=True) 
    paymentmode = models.CharField(max_length=2, choices=PAYMENT_MODE_CHOICES) 

    def __str__(self):
        return f'{self.id}: {self.customer.firstname} {self.customer.lastname}, {self.food.name}, {self.quantity}, {self.paymentmode}, {self.orderdatetime}'


class OrderItem(models.Model):

    quantity = models.IntegerField(default=1)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.order.customer.firstname} {self.order.customer.lastname}, {self.food.name}, {self.quantity}'

    def total_price(self):
        return self.food.price * self.quantity