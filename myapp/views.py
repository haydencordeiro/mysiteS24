from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from myapp.models import Book


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'booklist': booklist})

def about(request):
    return render(request, 'myapp/about0.html')
