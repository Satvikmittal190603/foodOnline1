from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import Userform
from .models import User
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
            messages.success(request,"your account has been successfully registered ")
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
