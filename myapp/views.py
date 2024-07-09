# Create your views here.
from django.shortcuts import render, redirect

from myapp.models import Book
from django.http import HttpResponse
from .forms import *
from .models import Book
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
import random


def index(request):
    last_login = request.session.get("last_login")
    if last_login:
        message = f"Your last login was at {last_login}"
    else:
        message = "Your last login was more than one hour ago"
    booklist = Book.objects.all().order_by("id")[:10]
    return render(
        request, "myapp/index.html", {"booklist": booklist, "message": message}
    )


def details(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, "myapp/details.html", {"book": book})


def about(request):
    lucky_num = request.COOKIES.get("lucky_num")
    if lucky_num:
        mynum = lucky_num
    else:
        mynum = random.randint(1, 100)
        response = render(request, "myapp/about.html", {"mynum": mynum})
        response.set_cookie("lucky_num", mynum, max_age=5 * 60)  # Expires in 5 minutes
        return response
    return render(request, "myapp/about.html", {"mynum": mynum})


def getFeedback(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_choices = form.cleaned_data["feedback"]
            choices_text = []
            for choice in feedback_choices:
                if choice == "B":
                    choices_text.append(" to borrow books.")
                elif choice == "P":
                    choices_text.append(" to purchase books.")
                else:
                    choices_text.append(" None.")
            return render(
                request, "myapp/fb_results.html", {"choices_text": choices_text}
            )
        else:
            return HttpResponse("Invalid data")
    else:
        form = FeedbackForm()
        return render(request, "myapp/feedback.html", {"form": form})


def get_category_name(category_id):
    for id, name in Book.CATEGORY_CHOICES:
        if id == category_id:
            return name
    return None  # or raise an exception if you prefer


def findbooks(request):

    if request.method == "POST":
        form = SearchForm(request.POST)  # No need to pass category_choices here
        if form.is_valid():
            name = form.cleaned_data.get("name", "")
            category_id = form.cleaned_data.get("category", None)
            print(category_id)
            max_price = form.cleaned_data["max_price"]

            if category_id:
                # Retrieve books for the selected category and max_price
                booklist = Book.objects.filter(
                    category=category_id, price__lte=max_price
                )
            else:
                # Retrieve all books with price <= max_price
                booklist = Book.objects.filter(price__lte=max_price)
            category = get_category_name(category_id)
            print(category)
            if not category_id:
                category = category_id
            # print(booklist)
            return render(
                request,
                "myapp/results.html",
                {
                    "name": name,
                    "category_id": category_id,
                    "booklist": booklist,
                    "category": category,
                },
            )
        else:
            return render(
                request,
                "myapp/findbooks.html",
                {"form": form, "message": "Invalid data"},
            )
    else:
        form = SearchForm()  # Create a blank form
        # form.fields['category'].choices = categories  # Set choices dynamically
        return render(request, "myapp/findbooks.html", {"form": form})


def place_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data["books"]
            order = form.save(commit=False)
            member = order.member
            type = order.order_type
            order.save()
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)
            return render(
                request, "myapp/order_response.html", {"books": books, "order": order}
            )
        else:
            return render(request, "myapp/placeorder.html", {"form": form})

    else:
        form = OrderForm()
        return render(request, "myapp/placeorder.html", {"form": form})


def review_view(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            if 1 <= rating <= 5:
                review = form.save()
                book = review.book
                book.num_reviews = book.num_reviews + 1
                book.save()
                return redirect("myapp:index")
            else:
                form.add_error("rating", "You must enter a rating between 1 and 5!")
    else:
        form = ReviewForm()
    return render(request, "myapp/review.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session["last_login"] = str(timezone.now())
                request.session.set_expiry(3600)  # Session expires in 1 hour
                return HttpResponseRedirect(reverse("myapp:index"))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details.")
    else:
        return render(request, "myapp/login.html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("myapp:index"))


@login_required
def chk_reviews(request, book_id):
    user = request.user
    # Check if the user is a member
    if Member.objects.filter(id=user.id).exists():
        try:
            book = Book.objects.get(pk=book_id)
            reviews = Review.objects.filter(book=book)
            if reviews.exists():
                avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
                return render(
                    request,
                    "myapp/chk_reviews.html",
                    {"avg_rating": avg_rating, "book": book},
                )
            else:
                return render(
                    request,
                    "myapp/chk_reviews.html",
                    {"message": "No reviews submitted for this book."},
                )
        except Book.DoesNotExist:
            return render(
                request, "myapp/chk_reviews.html", {"message": "Book not found."}
            )
    else:
        return render(
            request,
            "myapp/chk_reviews.html",
            {"message": "You are not a registered member!"},
        )
