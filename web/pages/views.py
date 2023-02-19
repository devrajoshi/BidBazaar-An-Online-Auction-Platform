from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required

from django.template import context

from .models import Item, User

# Create your views here.
def index(request):
    user = None
    if request.user.is_authenticated:
        user = DjangoUser.objects.get(id=request.user.id)
    bids = Item.objects.all()

    context = {"bids": bids, user: user}

    return render(request, "home.html", context)


def explore(request):
    bids = Item.objects.all()
    context = {"bids": bids}
    return render(request, "explore.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        errors = []

        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            userinDB = DjangoUser.objects.filter(email=email)
            if userinDB.exists():
                errors = ["Something went wrong!"]
                return render(request, "register.html", { "errors": errors })

            user = DjangoUser.objects.create(first_name=firstname, last_name=lastname, email=email, username=email)
            if user:
                user.set_password(password)
                user.save()
                return redirect("/login")
            else:
                errors = ["Something went wrong!"]
                return render(request, "register.html", {"errors": errors})
        else:
            errors = ["Passwords don't match!"]
            return render(request, "register.html", {"errors": errors})
    else:
        return render(request, "register.html")


def login(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        dbUser = DjangoUser.objects.filter(email=email)
        if dbUser:
            user = authenticate(username=email, password=password)
            if user:
                django_login(request, user)
                redirect_path_next = request.GET.get("next")
                if redirect_path_next:
                    return redirect(redirect_path_next)
                return redirect("/")
            else:
                errors = ["Username or passwords don't match!"]
                return render(request, "login.html", {"errors": errors})
        else:
            errors = ["Username or passwords don't match!"]
            return render(request, "login.html", {"errors": errors})
    else:
        return render(request, "login.html")


def item_page(request, item_id, item_slug):
    bid = Item.objects.get(id=item_id)
    if bid.slug != item_slug:
        return HttpResponseNotFound("404 Not Found")
    context = {"bid": bid}
    return render(request, "item_page.html", context)


@login_required(login_url="/login")
def post_item(request):
    return render(request, "post_item.html")


def user_profile(request, user_id):
    user_details = User.objects.get(id=user_id)
    context = {"user_details": user_details}
    return render(request, "profile/me_page.html", context)


def me_page(request):
    context = {}
    return render(request, "profile/me_page.html", context)

def logout(request):
    django_logout(request)
    return redirect("/")
