from django.urls import path
from myapp import views1

app_name = 'myapp'

urlpatterns = [
    path(r'', views1.about, name='index'),
    path(r'about', views1.about, name='about'),
    path(r'<int:book_id>', views1.details, name='details')
    ]
