from django.urls import path
from . import views

app_name='webkiosk'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('register/', views.registerpage, name='register'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutuser, name='logout'),
    
    #For regular non-admin users
    path('userprofile/', views.userprofile, name='userprofile'),
    # path('cart/', views.cart, name='cart'),
    path('userorders/', views.userorders, name='userorders'),
    path('userorderdetails/<int:pk>/', views.userorderdetails, name='userorderdetails'),
    path('userorderdetails/<int:pk>/edit', views.userorderupdate, name='userorderupdate'),
    path('userorderdetails/<int:pk>/delete', views.userorderdelete, name='userorderdelete'),
    path('userneworder/', views.userneworder, name='userneworder'),
    path('products/', views.products, name='products'),
    path('products/<int:pk>/', views.productdetail, name='productdetail'),
    
    # For admin users
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Food
    path('food/', views.listfood, name='food-list'),
    path('food/new/', views.createfood, name='food-create'),
    path('food/<int:pk>/', views.detailfood, name='food-detail'),
    path('food/<int:pk>/edit/', views.updatefood, name='food-edit'),
    path('food/<int:pk>/delete/', views.deletefood, name='food-delete'),
    
    # Customer
    path('customer/', views.listcustomer, name='customer-list'),
    path('customer/new/', views.createcustomer, name='customer-create'),
    path('customer/<int:pk>/', views.detailcustomer, name='customer-detail'),
    path('customer/<int:pk>/edit/', views.updatecustomer, name='customer-edit'),
    path('customer/<int:pk>/delete/', views.deletecustomer, name='customer-delete'),
    
    #Order
    path('order/', views.listorder, name='order-list'),
    path('order/new/', views.createorder, name='order-create'),
    path('order/<int:pk>/', views.detailorder, name='order-detail'),
    path('order/<int:pk>/edit/', views.updateorder, name='order-edit'),
    path('order/<int:pk>/delete/', views.deleteorder, name='order-delete'),
]
