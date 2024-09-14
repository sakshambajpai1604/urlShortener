from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import URL, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
import random
import string

def index(request):
    return render(request, 'indexurl.html')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "shortly/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")

def shorten_url(request):
    if request.method == 'POST':
        orignal_url = request.POST.get('orignal_url')
       
        existing_url = URL.objects.filter(orignal_url=orignal_url).first()
        if existing_url:
            short_url = request.build_absolute_uri('/') + existing_url.short_url
            return render(request, 'indexurl.html', {'short_url': short_url})
        
        short_code = generate_short_code()
        short_url = request.build_absolute_uri('/') + short_code
        URL.objects.create(orignal_url=orignal_url, short_url=short_code)
        return render(request, 'indexurl.html', {'short_url': short_url})
    return redirect('index')

def redirect_original_url(request, short_url):
    orignal_url = URL.objects.get(short_url=short_url).orignal_url
    return redirect(orignal_url)

def generate_short_code():
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for i in range(6))
    while URL.objects.filter(short_url=short_code).exists():
        short_code = ''.join(random.choice(characters) for i in range(6))
    return short_code