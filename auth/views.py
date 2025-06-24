from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required



# Create your views here.
def login(request):
    
    if request.method == 'POST':
        if request.POST['username'] is None or request.POST['password'] is None:
            messages.info(request, 'Please complete username and password')
            return redirect('login')
        else:
            user_login = auth.authenticate(request, username=request.POST['username'], password = request.POST['password'])
            if user_login is not None:
                auth.login(request, user_login)
                return redirect('/')
            else:
                messages.info(request, 'Username/password incorrect')
                return redirect('login')
        
        
        
    return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        
        #validate fields
        if password != confirmpassword:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
        else:
            #Check if email is taken
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already in use')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already in use')
                return redirect('signup')
            else:
                #Create user and save to DB
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                #login
                user_login = auth.authenticate(request, username=username, password=password)
                if user_login is not None:
                    auth.login(request, user_login)
                    return redirect('/')
                else:
                    messages.info(request, 'An error occurred, try again later')
                    return redirect('signup')
                                        
    else:
        return render(request, 'signup.html')
                            
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')