from django.urls import path
from myapp import views


app_name = 'myapp'

urlpatterns = [
    path(r'', views.about, name='index'),
    path(r'<int:book_id>', views.details, name='details'),
    path(r'about/', views.about, name='about'),
    path('feedback/', views.getFeedback, name='feedback1'),
    path('findbooks/', views.findbooks, name='findbooks'),
]
