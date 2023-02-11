from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound

import datetime

from .models import Item, User

# Create your views here.
def index(request):
    bids = Item.objects.all()
    context = {
        "bids": bids
        }
    return render(request, "home.html", context)


def explore(request):
    bids = Item.objects.all()
    context = {"bids": bids}
    return render(request, "explore.html", context)


def register(request):
    if request.method == "POST":
        errors = []

        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            user = User.objects.create(firstname=firstname, lastname=lastname, email=email, password=confirm_password)

            if user:
                return redirect("/login")
            else:
                errors = ["Something went wrong!"]
                return render(request, "register.html", { "errors": errors })
        else:
            errors = ["Passwords don't match!"]
            return render(request, "register.html", { "errors": errors })
    else:
        return render(request, "register.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = User.objects.get(email=email)
        if user:
            if(user.password == password):
                return redirect("/")
            else:
                errors = ["Username or passwords don't match!"]
                return render(request, "login.html", { "errors": errors })
        else:
            errors = ["Username or passwords don't match!"]
            return render(request, "login.html", { "errors": errors })
    else:
        return render(request, "login.html")

def item_page(request, item_id, item_slug):
    bid = Item.objects.get(id=item_id)
    if bid.slug != item_slug:
        return HttpResponseNotFound("404 Not Found")
    context = {"bid": bid}
    return render(request, "item_page.html", context)

def Post(request):
    return render(request,'post.html')

def user_profile(request, user_id):
    return render(request, "user_profile.html")
