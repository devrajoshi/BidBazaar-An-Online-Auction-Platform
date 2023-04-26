from django.contrib import messages
import json
import datetime
from django.utils import timezone
import pytz
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, JsonResponse
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from faker import Faker

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import pandas as pd

from .forms import PostItem
from .models import Item, User, Bid

def index(request):
    # fake = Faker()

    # for _ in range(0, 5):
    #     title = fake.name()
    #     item = {
    #         "title": title,
    #         "description": fake.sentence(),
    #         "image": fake.image_url(),
    #         "price": random.uniform(0, 10000),
    #         "seller_id": 1,
    #         "deadline_at": fake.date_time(),
    #         "slug": slugify(title)
    #     }
    #     Item.objects.create(**item)

    user = None
    if request.user.is_authenticated:
        user = DjangoUser.objects.get(id=request.user.id)

    hot_bids = Item.objects.filter(
        starts_at__lte=timezone.now()
    ).order_by(
        "-pk"
    )
    upcoming_bids = Item.objects.filter(
        starts_at__gt=timezone.now()
    ).order_by("-pk")

    context = {
            "hot_bids": hot_bids,
            "upcoming_bids": upcoming_bids,
            "user": user
    }

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
                first_name=firstname,
                last_name=lastname,
                email=email, username=email
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

def recommend_items(item_id):
    items = Item.objects.all()

    # Preprocess title and description fields
    preprocessed_text = []
    for item in items:
        text = f'{item.title} {item.description}'
        # Tokenize
        tokens = text.split()
        # Remove stop words
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if not word.lower() in stop_words]
        # Stemming
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word) for word in tokens]
        # Combine processed title and description
        preprocessed_text.append(' '.join(tokens))

    # Compute TF-IDF feature vectors
    vectorizer = TfidfVectorizer()
    features = vectorizer.fit_transform(preprocessed_text)

    # Compute pairwise similarities
    similarities = cosine_similarity(features)

    # Convert similarities to a pandas DataFrame
    df_similarities = pd.DataFrame(similarities, index=[item.id for item in items], columns=[item.id for item in items])

    # Get item ID and similarity scores for a given item ID
    similar_items = df_similarities[item_id].sort_values(ascending=False)[:10]
    return similar_items


def item_page(request, item_id, item_slug):
    bid = Item.objects.get(id=item_id)
    if not bid:
        return HttpResponseNotFound("404 Not Found")
    if bid.slug != item_slug:
        return HttpResponseNotFound("404 Not Found")
    recommended = recommend_items(bid.id).index
    recommended_items = Item.objects.filter(id__in=recommended.tolist()[:4])
    bids = Bid.objects.filter(item_id=bid.id)
    context = {"bid": bid, "bids": bids, "recommended_items": recommended_items}
    return render(request, "item_page.html", context)


@login_required(login_url="/login")
def post_item(request):
    if request.method == "POST":
        post_item_form = PostItem(request.POST, request.FILES)

        try:
            if post_item_form.is_valid():
                item = post_item_form.save(commit=False)
                for _, field_value in post_item_form.cleaned_data.items():
                    if not field_value:
                        messages.error(request,
                                       "Please enter all the details!")
                        return render(
                            request, "post_item.html", {"form": post_item_form}
                        )
                if item.deadline_at > pytz.timezone("Asia/Kathmandu").localize(
                    datetime.datetime.now()
                ):
                    item.slug = slugify(item.title)
                    item.starts_at = datetime.datetime.now()
                    item.seller_id = request.user.id
                    item.save()

                    return redirect("/")
                else:
                    messages.error(
                            request,
                            "Cannot create an auction in the past!"
                    )
                    return render(
                            request,
                            "post_item.html",
                            {"form": post_item_form}
                    )
            else:
                messages.error(request, "Check all the details again!")
                return render(
                        request,
                        "post_item.html",
                        {"form": post_item_form}
                )
        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong")
            return render(request, "post_item.html", {"form": post_item_form})

    form = PostItem()
    return render(request, "post_item.html", {"form": form})


@login_required(login_url="/login")
def bid(request, item_id):
    body = json.loads(request.body.decode())
    amount = int(body.get("amount"))
    bidder = request.user
    item = Item.objects.get(id=item_id)
    if request.user.id == item.seller.id:
        return JsonResponse(
            {
                "success": False,
                "message": "You can't bid your own product!"
            }
        )
    bids = Bid.objects.order_by("-id")
    if bids:
        if request.user.id == bids[0].bidder.id and bids[0].item.id == item_id:
            return JsonResponse(
                {
                    "success": False,
                    "message": "You are the highest bidder currently!"
                }
            )
        if bids[0].item.id == item_id and amount <= int(bids[0].amount):
            return JsonResponse(
                {
                    "success": False,
                    "message": "Please bid higher than the current bid!"
                }
            )
    Bid.objects.create(item_id=item_id, amount=amount, bidder_id=bidder.id)
    return JsonResponse({"success": True, "message": "success"})


@login_required(login_url="/login")
def user_profile(request, user_id):
    try:
        user_details = DjangoUser.objects.get(id=user_id).profile
        context = {"user_details": user_details}
        return render(request, "profile/me_page.html", context)
    except Exception as e:
        print(e)
        return HttpResponseNotFound("404 Not Found")


@login_required(login_url="/login")
def logout(request):
    django_logout(request)
    return redirect("/")


def search(request):
    if request.method == "GET":
        query = request.GET.get("q")
        query_safe = query.lower()
        bids = Item.objects.filter(
            Q(description__icontains=query_safe) | Q(title__icontains=query_safe)
        )
        context = {"query": query, "bids": bids}
        return render(request, "search.html", context)
