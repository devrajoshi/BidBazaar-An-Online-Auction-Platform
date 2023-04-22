from django.contrib import messages
import json
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponseNotFound, JsonResponse
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from faker import Faker

from .forms import PostItem
from .models import Item, User, Bid


def index(request):
    # fake = Faker()

    # for _ in range(0, 5):
    #    title = fake.name()
    #    item = {
    #        "title": title,
    #        "description": fake.sentence(),
    #        "image": fake.image_url(),
    #        "price": random.uniform(0, 10000),
    #        "seller_id": 1,
    #        "deadline_at": fake.date_time(),
    #        "slug": slugify(title)
    #    }
    #    Item.objects.create(**item)

    user = None
    if request.user.is_authenticated:
        user = DjangoUser.objects.get(id=request.user.id)
    bids = Item.objects.all()

    context = {"bids": bids, "user": user}

    return render(request, "home.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            userinDB = DjangoUser.objects.filter(email=email)
            if userinDB.exists():
                messages.error(request, "User already exists!")
                return render(request, "register.html")

            user = DjangoUser.objects.create(
                first_name=firstname, last_name=lastname, email=email, username=email
            )
            site_user = User.objects.create(user_id=user.pk)
            if user and site_user:
                user.set_password(password)
                user = user.save()
                site_user.save()
                messages.success(request, "User registered successful!")
                return redirect("/login")
            else:
                messages.error(request, "Something went wrong!")
                return render(request, "register.html")
        else:
            messages.error(request, "Passwords don't match!")
            return render(request, "register.html")
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
                messages.error(request, "Username or passwords don't match!")
                return render(request, "login.html")
        else:
            messages.error(request, "Username or passwords don't match!")
            return render(request, "login.html")
    else:
        errors = []
        redirect_path_next = request.GET.get("next")
        if redirect_path_next:
            messages.info(request, "Please login to continue!")
        return render(request, "login.html", {"errors": errors})


def item_page(request, item_id, item_slug):
    bid = Item.objects.get(id=item_id)
    if not bid:
        return HttpResponseNotFound("404 Not Found")
    if bid.slug != item_slug:
        return HttpResponseNotFound("404 Not Found")
    bids = Bid.objects.filter(item_id=bid.id)
    context = {"bid": bid, "bids": bids}
    return render(request, "item_page.html", context)


@login_required(login_url="/login")
def post_item(request):
    if request.method == "POST":
        post_item_form = PostItem(request.POST, request.FILES)

        if post_item_form.is_valid():
            item = post_item_form.save(commit=False)
            item.slug = slugify(item.title)
            item.seller_id = request.user.id
            item.save()

            return redirect("/")
        else:
            print("form not valid")

    form = PostItem()
    return render(request, "post_item.html", {"form": form})


@login_required(login_url="/login")
def bid(request, item_id):
    body = json.loads(request.body.decode())
    amount = float(body.get("amount"))
    bidder = request.user
    item = Item.objects.get(id=item_id)
    if request.user.id == item.seller.id:
        return JsonResponse(
            {"success": False, "message": "You can't bid your own product!"}
        )
    bids = Bid.objects.order_by("-id")
    if bids:
        if request.user.id == bids[0].bidder.id:
            return JsonResponse(
                {"success": False, "message": "You are the highest bidder currently!"}
            )
        if amount <= float(bids[0].amount):
            return JsonResponse(
                {"success": False, "message": "Please bid higher than the current bid!"}
            )
    Bid.objects.create(item_id=item_id, amount=amount, bidder_id=bidder.id)
    return JsonResponse({"success": True, "message": "success"})


@login_required(login_url="/login")
def user_profile(request, user_id):
    try:
        user_details = User.objects.get(id=user_id)
        context = {"user_details": user_details}
        return render(request, "profile/me_page.html", context)
    except:
        return HttpResponseNotFound("404 Not Found")


@login_required(login_url="/login")
def logout(request):
    django_logout(request)
    return redirect("/")


def search(request):
    if request.method == "GET":
        query = request.GET.get("q")
        bids = Item.objects.filter(
            Q(description__contains=query) | Q(title__contains=query)
        )
        context = {"bids": bids}
        return render(request, "search.html", context)
