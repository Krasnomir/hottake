from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *

def home(request):
    template = loader.get_template('app/home.html')
    context = {
        'content':"Welcome to the home page!"
    }
    return HttpResponse(template.render(context, request))

def index(request):
    return redirect('home')

def login_view(request):
    template = loader.get_template('app/login.html')

    # handle POST request
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # check if a user with that username exists in the database
        if not User.objects.filter(username=username).exists():
            context = {'message':"Invalid username"}
            return HttpResponse(template.render(context, request))
        
        # check if the provided password is correct
        user = authenticate(username=username, password=password)
        
        if user is None:
            context = {'message':"Invalid password"}
            return HttpResponse(template.render(context, request))
        else:
            login(request, user)
            return redirect('/home/')
    
    # handle GET request - display the normal page
    context = {'message':""}
    return HttpResponse(template.render(context, request))

def register_view(request):
    template = loader.get_template('app/register.html')

    # handle POST request
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # check if a user with that usernmae exists
        user = User.objects.filter(username=username)
        if user.exists():
            context = {'message':"Username is already taken"}
            return HttpResponse(template.render(context, request))
        
        # create a new user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        
        # set the user password
        user.set_password(password)
        user.save()
        
        context = {'message':"Account created successfuly"}
        return HttpResponse(template.render(context, request))
    
    #handle GET request
    context = {'message':""}
    return HttpResponse(template.render(context, request))
