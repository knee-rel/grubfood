from django.contrib.auth.forms import UserCreationForm
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Customer, Food, Order, OrderItem
from .forms import FoodForm, CustomerForm, OrderForm, OrderItemForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.
# main views
def index(request):
    return render(request, 'webkiosk/welcome.html')

def about(request):
    return render(request, 'webkiosk/about.html')

@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
            )
            
            messages.success(request, 'Account was created for ' + username)
            
            return redirect('webkiosk:login')
        
    context = {'form':form}
    return render(request, 'webkiosk/register.html', context)

@unauthenticated_user
def loginpage(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('webkiosk:dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')
    context = {}
    return render(request, 'webkiosk/signin.html', context)
    
def logoutuser(request):
    logout(request)
    return redirect('webkiosk:login')

#################
# customer views
@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def userprofile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            
    context={'form':form}
    return render(request, 'webkiosk/user_profile.html', context)

def products(request):
    context = {
        'products': Food.objects.all()
    }
    return render(request, 'webkiosk/user_products.html', context)

def productdetail(request, pk):
    product = Food.objects.get(id=pk)
    context = {'product':product}
    return render(request, 'webkiosk/product_details.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def userorders(request):
    orders = request.user.customer.order_set.all()
    
    total_orders = orders.count()
    
    context={'orders':orders, 'total_orders':total_orders}
    return render(request, 'webkiosk/user_orders.html', context)
    
@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def userorderdetails(request, pk):
    orderinfo = Order.objects.get(id=pk)
    # order = OrderItem.objects.filter(id=pk)
    order = OrderItem.objects.filter(order=pk)
    totalprice = 0
    for orderitem in order:
        totalprice += orderitem.food.price * orderitem.quantity
    context = {'order': order, 'orderinfo': orderinfo, 'totalprice': totalprice}
    return render(request, 'webkiosk/user_order_details.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def userneworder(request):
    if request.method == 'GET':
        form = OrderForm()
    elif request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webkiosk:userorders')
    context = {'form':form}
    return render(request, 'webkiosk/user_new_order.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def userorderupdate(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'GET':
        form = OrderForm(instance=order)
    elif request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order successfully updated')
            return redirect('webkiosk:userorders')
    context = {'form':form}
    return render(request, 'webkiosk/user_new_order.html', context)


@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def userorderdelete(request, pk):
    order = OrderItem.objects.get(id=pk)
    if request.method == 'GET':
        context = {'order':order}
        return render(request, 'webkiosk/user_delete_order.html', context)
    elif request.method == 'POST':
        order.delete()
        return redirect('webkiosk:products')
    
@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def usernewitem(request, pk):
    if request.method == 'GET':
        form = OrderItemForm(initial={'order': pk})
        context = {'form':form}
        return render(request, 'webkiosk/user_item_new.html', context)
    
    elif request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webkiosk:userorderdetails')
        
@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def userupdateitem(request, pk):
    # orderitem = OrderItem.objects.get(id=pk)
    # form = OrderItemForm(instance=orderitem)
    
    # if request.method == 'POST':
    #     form = OrderItemForm(request.POST, request.FILES, instance=orderitem)
    #     if form.is_valid:
    #         form.save()
    #         messages.success(request, 'Update Sucessful!')
            
    # context = {'form': form, 'orderitem': orderitem}
    # return render(request, 'webkiosk/user_item_new.html', context)
    
    orderitem = OrderItem.objects.get(id=pk)
    if request.method == 'GET':
        form = OrderItemForm(instance=orderitem)
    elif request.method == 'POST':
        form = OrderItemForm(request.POST, instance=orderitem)
        if form.is_valid:
            form.save()
            messages.success(request, 'Update Sucessful!')
    context = {'form': form, 'orderitem': orderitem}
    return render(request, 'webkiosk/user_item_new.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['customer'])
def userdeleteitem(request, pk):
    orderitem = OrderItem.objects.get(id=pk)
    if request.method == 'GET':
        context = {'orderitem': orderitem}
        return render(request, 'webkiosk/user_item_delete.html', context)
    elif request.method == 'POST':
        orderitem.delete()
        return redirect('webkiosk:userorders')


#############
# admin views
@admin_only
@login_required(login_url='webkiosk:login')
def dashboard(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    foods = Food.objects.all()
    
    total_orders = orders.count()
    total_customers = customers.count()
    total_foods = foods.count()
    
    context={'orders':orders, 'customers':customers, 'total_orders':total_orders, 'total_customers':total_customers, 'total_foods':total_foods}
    
    return render(request, 'webkiosk/dashboard.html', context)

# food views
@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def listfood(request):
    context = {
        'foodlist': Food.objects.all(),
    }
    return render(request, 'webkiosk/food.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def createfood(request):
    if request.method == 'GET':
        form = FoodForm()
    elif request.method == 'POST':
        #insert new form record
        form = FoodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webkiosk:food-list')
        
    context = {'form':form}
    return render(request, 'webkiosk/food_form.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def detailfood(request, pk):
    food = Food.objects.get(id=pk)
    # orderinfo = Order.objects.get(id=pk)
    # orders = OrderItem.objects.filter(food=pk)
    # for orderitem in order:
    #     totalprice += orderitem.food.price * orderitem.quantity
        
    context = {'food':food}
    return render(request, 'webkiosk/food_detail.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def updatefood(request, pk):
    food = Food.objects.get(id=pk)
    if request.method == 'GET':
        form = FoodForm(instance=food)
    elif request.method == 'POST':
        form = FoodForm(request.POST, instance=food)
        if form.is_valid():
            form.save()
            messages.success(request, 'Food record successfully updated')
    context = {'form':form}
    return render(request, 'webkiosk/food_form.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def deletefood(request,pk):
    food = Food.objects.get(id=pk)
    if request.method == 'GET':
        context = {'food':food}
        return render(request, 'webkiosk/food_delete.html', context)
    elif request.method == 'POST':
        food.delete()
        return redirect('webkiosk:food-list')
    
    
# customer views
@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def listcustomer(request):
    context = {
        'customerlist': Customer.objects.all()
    }
    return render(request, 'webkiosk/customer.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def createcustomer(request):
    if request.method == 'GET':
        form = CustomerForm()
    elif request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webkiosk:customer-list')
    context = {'form':form}
    return render(request, 'webkiosk/customer_form.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def detailcustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = Order.objects.filter(customer__id=pk)
    context = {'customer':customer, 'orders':orders}
    return render(request, 'webkiosk/customer_detail.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def updatecustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        form = CustomerForm(instance=customer)
    elif request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer successfully updated')
    context = {'form':form}
    return render(request, 'webkiosk/customer_form.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def deletecustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'GET':
        context = {'customer':customer}
        return render(request, 'webkiosk/customer_delete.html', context)
    elif request.method == 'POST':
        customer.delete()
        return redirect('webkiosk:customer-list')     
      
# order views
@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def listorder(request):
    context = {
        'orderlist': Order.objects.all()
    }
    return render(request, 'webkiosk/order.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def createorder(request):
    if request.method == 'GET':
        form = OrderForm()
    elif request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webkiosk:order-list')
    context = {'form':form}
    return render(request, 'webkiosk/order_form.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def detailorder(request, pk):
    orderinfo = Order.objects.get(id=pk)
    order = OrderItem.objects.filter(order=pk)
    totalprice = 0
    for orderitem in order:
        totalprice += orderitem.food.price * orderitem.quantity
    context = {'order': order, 'orderinfo': orderinfo, 'totalprice': totalprice}
    return render(request, 'webkiosk/order_detail.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def updateorder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'GET':
        form = OrderForm(instance=order)
    elif request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order successfully updated')
    context = {'form':form}
    return render(request, 'webkiosk/order_form.html',context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def deleteorder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'GET':
        context = {'order':order}
        return render(request, 'webkiosk/order_delete.html', context)
    elif request.method == 'POST':
        order.delete()
        return redirect('webkiosk:order-list')
    
# order item views
@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def addorderitem(request, pk):
    if request.method == 'GET':
        form = OrderItemForm(initial={'order': pk})
        context = {'form':form}
        return render(request, 'webkiosk/orderitem_form.html', context)
    
    elif request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webkiosk:order-list')

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def updateorderitem(request, pk):
    orderitem = OrderItem.objects.get(id=pk)
    if request.method == 'GET':
        form = OrderItemForm(instance=orderitem)
    elif request.method == 'POST':
        form = OrderItemForm(request.POST, instance=orderitem)
        if form.is_valid:
            form.save()
            messages.success(request, 'Update Sucessful!')
    context = {'form': form, 'orderitem': orderitem}
    return render(request, 'webkiosk/orderitem_form.html', context)

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
def deleteorderitem(request, pk):
    orderitem = OrderItem.objects.get(id=pk)
    if request.method == 'GET':
        context = {'orderitem': orderitem}
        return render(request, 'webkiosk/orderitem_delete.html', context)
    elif request.method == 'POST':
        orderitem.delete()
        return redirect('webkiosk:order-list')