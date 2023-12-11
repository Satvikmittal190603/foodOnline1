from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('registerUser/',views.registerUser,name="registerUser"),
    path('registerVendor/',views.registerVendor,name="registerVendor"),
    
    path('login/',views.login,name="login"),
    path('logout/',views.logout,name="logout"),
    path('myAccount/',views.myAccount,name="myAccount"),
    
    
    path('vendorDashboard/',views.vendorDashboard,name="vendorDashboard"),
    path('custDashboard/',views.custDashboard,name="custDashboard"),
    
]
