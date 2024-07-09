from django.urls import path
from myapp import views


app_name = "myapp"

urlpatterns = [
    path(r"", views.index, name="index"),
    path(r"<int:book_id>", views.details, name="details"),
    path(r"about/", views.about, name="about"),
    path("feedback/", views.getFeedback, name="feedback1"),
    path("findbooks/", views.findbooks, name="findbooks"),
    path("place_order", views.place_order, name="place_order"),
    path("review/", views.review_view, name="review"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("chk_reviews/<int:book_id>/", views.chk_reviews, name="chk_reviews"),
]
