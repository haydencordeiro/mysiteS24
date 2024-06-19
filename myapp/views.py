from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from myapp.models import Book


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})
def details(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'myapp/details.html', {'book': book})

def about(request):
    return render(request, 'myapp/about.html')
