from django.shortcuts import render,redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from accounts.forms import Userform
from accounts.models import User, UserProfile
from django.contrib import messages 
# Create your views here.

def registerUser(request):
    if request.method == 'POST':
        print(request.POST) 
        form =Userform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password=  form.cleaned_data['password']
            user.role = User.CUSTOMER
            user.set_password(password)  #HAsh the Password
            user.save()
            messages.success(request,"your account has been successfully registered!")
            return redirect('registerUser')
        else:
            print('invalid')
            print(form.errors)
    else:         
        form = Userform()
    context = {
        'form':form
    }
    return render(request,"accounts/registerUser.html",context)



def registerVendor(request):
    if request.method == 'POST':
       # print(request.POST) 
        form =Userform(request.POST)
        v_form = VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            user = form.save(commit=False)
            password=  form.cleaned_data['password']
            user.role = User.RESTAURANT
            user.set_password(password)  #HAsh the Password
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request,"your account has been successfully registered! Please Wait for the approval !")
            return redirect('registerVendor')
        else:
            print('invalid')
            print(form.errors)
    else:         
        form = Userform()
        v_form = VendorForm()
    
    context ={
        'form':form,
        'v_form':v_form,
    }
    
    return render(request,"accounts/registerVendor.html",context)