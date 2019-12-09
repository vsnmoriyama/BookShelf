from django.http import HttpResponse
from .models import book  # 追加する
from .forms import BookSearchFormSet

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views import generic


def booklist_template(request):
    d = {
        'book_list': book.objects.all(),
    }
    return render(request, 'bookList/index.html', d)

def index(request):

    print('パラメータ:')
    print('(' + request.GET['isbn'] + ')')
    print('(' + request.GET['picture_name']+ ')')
    print('(' + request.GET['title']+ ')')
    print('(' + request.GET['author']+ ')')
    print('(' + request.GET['publisher']+ ')')
    print('(' + request.GET['pubdate']+ ')')

    d = {
        'book_list': book.objects.all(),
    }

    booklist_isbn = book.objects.get(isbn = request.GET['isbn'])

    print(booklist_isbn.author)

#-------------------------------------------------------------------------

    values = [1, 2]

    # Turn list of values into list of Q objects
    queries = [Q(pk=value) for value in values]

    # Take one Q object from the list
    query = queries.pop()

    # Or the Q object with the ones remaining in the list
    for item in queries:
        query |= item

    # Query the model
    # print('*' + book.objects.filter(query))

#------------------------------------------------------------------------

    # result = book.objects.all()
    result = book.objects.filter(Q(isbn = request.GET['isbn']))
    for data in result:
        print('isbn = ' + data.isbn)
        print('picture_name = ' + data.picture_name)
        print('title = ' + data.title)

    return render(request, 'bookList/index.html', d)
