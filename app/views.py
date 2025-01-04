import json
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from .validation import validate
from datetime import datetime

def home(request):
    if request.method == "POST":
        # JSON containg info about the user's vote
        data = json.loads(request.body)

        post_id = data.get('post_id')
        vote_type = data.get('vote_type')

        post = Post.objects.get(id=post_id)

        userPreviousVote = post.get_user_vote(request.user)

        if userPreviousVote is None:
            post.set_user_vote(request.user, vote_type)

            if vote_type == "downvote":
                post.downvotes = post.downvotes + 1
                post.save()
                return JsonResponse({"msg": 3}) # downvoted for the first time
            else:
                post.upvotes = post.upvotes + 1
                post.save()
                return JsonResponse({"msg": 4}) # upvoted for the first time
        
        elif userPreviousVote == "upvote":
            if vote_type == "upvote":
                return JsonResponse({"msg": -1}) # fail
            else:
                post.set_user_vote(request.user, vote_type)
                post.upvotes = post.upvotes - 1
                post.downvotes = post.downvotes + 1
                post.save()
                return JsonResponse({"msg": 1}) # downvoted
            
        else:  # userPreviousVote == "downvote"
            if vote_type == "downvote":
                return JsonResponse({"msg": -1}) # fail
            else:
                post.set_user_vote(request.user, vote_type)
                post.downvotes = post.downvotes - 1
                post.upvotes = post.upvotes + 1
                post.save()
                return JsonResponse({"msg": 2}) # upvoted

    template = loader.get_template('app/posts.html')

    posts = Post.objects.all().order_by('-date')
    context = {
        'posts':posts,
        'user':request.user
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
        
        # validate all the fields
        validationMessage = validate(username, password, email, first_name, last_name)
        if validationMessage != 0:
            context = {'message':validationMessage}
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

def create_post(request):
    template = loader.get_template('app/create-post.html')

    if request.method == 'POST':
        user = request.user
        title = request.POST.get('title')
        body = request.POST.get('body')
        time = datetime.now()

        if len(title) == 0:
            context = {'message': "Title can't be empty"}
            return HttpResponse(template.render(context,request))
        elif len(body) == 0:
            context = {'message': "Post body/description can't be empty"}
            return HttpResponse(template.render(context,request))

        post = Post.objects.create (
            author = user,
            title = title,
            body = body,
            date = time
        )

        post.save()

        return redirect('/home/')

    return HttpResponse(template.render({},request));

def user_info(request, username):
    template = loader.get_template('app/user.html')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        context = {'message': "Couldn't find a user with that username"}

    posts = Post.objects.filter(author=user).order_by('-date')

    context = {
        'username':username,
        'date':user.date_joined,
        'posts':posts,
        'user':user
    }

    return HttpResponse(template.render(context, request));

# displays a page with post and its comments
def post_info(request, post_id):

    if request.method == "POST":
        user = request.user
        body = request.POST.get('body')
        time = datetime.now()

        if len(body) == 0:
            template = loader.get_template('app/post.html')
            context = {
                "post": Post.objects.get(pk=post_id),
                "comments": Comment.objects.filter(post=Post.objects.get(pk=post_id))
            }

        comment = Comment.objects.create (
            post = Post.objects.get(pk=post_id),
            author = user,
            body = body,
            date = time
        )

        comment.save()

        return redirect(post_info, post_id=post_id)

    template = loader.get_template('app/post.html')
    context = {
        "post": Post.objects.get(pk=post_id),
        "comments": Comment.objects.filter(post=Post.objects.get(pk=post_id))
    }
    
    return HttpResponse(template.render(context, request))