from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from myapp.models import Book
from django.http import HttpResponse
from .forms import FeedbackForm
from .forms import SearchForm
from .models import Book, Category



def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})
def details(request, book_id):
    book = Book.objects.get(pk=book_id)
    return render(request, 'myapp/details.html', {'book': book})

def about(request):
    booklist = Book.objects.all()
    return render(request, 'myapp/about.html', {'booklist': booklist})

def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else: choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice':choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form':form})


def findbooks(request):
    categories = []  # Adjust to fetch actual categories from your database

    if request.method == 'POST':
        form = SearchForm(request.POST)  # No need to pass category_choices here
        if form.is_valid():
            name = form.cleaned_data.get('name', '')
            category_id = form.cleaned_data.get('category', '')
            max_price = form.cleaned_data['max_price']

            if category_id:
                # Retrieve books for the selected category and max_price
                booklist = Book.objects.filter(category_id=category_id, price__lte=max_price)
            else:
                # Retrieve all books with price <= max_price
                booklist = Book.objects.filter(price__lte=max_price)

            return render(request, 'myapp/results.html',
                          {'name': name, 'category_id': category_id, 'booklist': booklist})
        else:
            return render(request, 'myapp/findbooks.html', {'form': form, 'message': 'Invalid data'})
    else:
        form = SearchForm()  # Create a blank form
        form.fields['category'].choices = categories  # Set choices dynamically
        return render(request, 'myapp/findbooks.html', {'form': form})
