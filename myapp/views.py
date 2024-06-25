from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from myapp.models import Book
from django.http import HttpResponse
from .forms import FeedbackForm


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
