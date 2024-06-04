# Import necessary classes
from django.http import HttpResponse
from .models import Publisher, Book, Member, Order

# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('pk','-publisher__city')
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>'+ str(book.id) + ': ' + str(book)+ ': ' + str(book.publisher.name)+ ': ' + str(book.publisher.city) + '</p>'
        response.write(para)
    return response


def about(request):
    response = HttpResponse()
    response.write('<p> This is an eBook APP. </p>')
    return response

def details(request,book_id):
    book = Book.objects.get(pk=book_id)
    response = HttpResponse()
    para = '<p>' + str(book.id) + ': ' + str(book.title.upper()) + ': $' + str(book.price) + ': ' + str(
        book.publisher.name) + '</p>'
    response.write(para)
    return response


