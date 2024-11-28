from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader

def home(request):
    template = loader.get_template('app/home.html')
    context = {
        'content':"Welcome to the home page!"
    }
    return HttpResponse(template.render(context, request))

def index(request):
    return redirect('home')
