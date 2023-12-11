from django.shortcuts import render,redirect
from django.http import HttpResponse

from vendor.forms import VendorForm
from accounts.forms import Userform
from accounts.models import User, UserProfile
from django.contrib import messages ,auth 
from .utils import detectUser
from django.contrib.auth.decorators import login_required ,user_passes_test
from django.core.exceptions import PermissionDenied
# Create your views here.

#Restrict vendor to access the customer dashboard

def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied

#Restrict customer to access the vendor dashboard
def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect("myAccount")
    elif request.method == 'POST':
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
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect("myAccount")
    elif request.method == 'POST':
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


def login(request):
    
    if request.user.is_authenticated:
        messages.warning(request,"You are already logged in!")
        return redirect("myAccount")
    
    elif request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        
        user = auth.authenticate(email=email,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,"you are logged in")
            return redirect('myAccount')
        else:
            messages.error(request,"invalid login credentials")
            return redirect('login')
    return render(request,"accounts/login.html")

def logout(request):
    auth.logout(request)
    messages.info(request,"you are logged out")
    return redirect('login')
    #return render(request,"accounts/logout.html")

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirecturl = detectUser(user)
    return redirect(redirecturl)

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,"accounts/custDashboard.html")

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request,"accounts/vendorDashboard.html")