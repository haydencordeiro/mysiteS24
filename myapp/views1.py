# Import necessary classes
from django.http import HttpResponse
from .models import Publisher, Book, Member, Order

# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('pk')[:10]
    heading1 = '<p>' + 'List of available books (order by Primary Key): ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>'+ str(book.id) + ': ' + str(book.title) + '</p>'
        response.write(para)

    linebreak = '<hr>'
    response.write(linebreak)

    publishers = Publisher.objects.all().order_by('city')
    heading2 = '<p>' + 'List of available publishers (order by City): ' + '</p>'
    response.write(heading2)
    for publisher in publishers:
        publisher_name = publisher.name
        publisher_city = publisher.city
        pub = '<p>'+ str(publisher_name) + ': ' + str(publisher_city) + '</p>'
        response.write(pub)
    return response

def about(request):
    response = HttpResponse()
    text = 'This is an eBook APP'
    response.write(text)
    return response


def detail(request, book_id):
    print(book_id)
    response = HttpResponse()
    booklist = Book.objects.filter(id=book_id)
    if booklist[0]:
        title = booklist[0].title.upper()
        price = '$' + str(booklist[0].price)
        publish = booklist[0].publisher.name
        det = '<p>' + 'Title: ' + title + '</p>'
        det2 = '<p>' + 'Price: ' + price + '</p>'
        det3 = '<p>' + 'Publisher: ' + publish + '</p>'
        response.write(det)
        response.write(det2)
        response.write(det3)

    return response