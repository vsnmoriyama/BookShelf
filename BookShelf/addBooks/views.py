import sys

from django.shortcuts import render, get_object_or_404

sys.path.append('../')
from bookList.models import book

from . import form


def newBook(request):
    return render(request, 'addBooks/addBooks.html', {'book': book(), 'form': form.AddBookForm()})


def addBook(request):
    # formの取得
    formData = form.AddBookForm(request.POST or None)
    if formData.is_valid(): # 入力チェック
        isbnCode = request.POST['isbn']
        if book.objects.filter(isbn=isbnCode).exists():
            books = book.objects.get(isbn=isbnCode)
            books.picture_name = request.POST['picture_name']
            books.title = request.POST['title']
            books.auther = request.POST['auther']
            books.publisher = request.POST['publisher']
            books.pubdate = request.POST['pubdate']
            message = 'update Book'

        else:

            books = book(isbn=request.POST['isbn'], picture_name=request.POST['picture_name'],
                         title=request.POST['title'], auther=request.POST['auther'],
                         publisher=request.POST['publisher'], pubdate=request.POST['pubdate'])
            message = 'add Book'

        books.save()
        return render(request, 'addBooks/addBooks.html', {
            'form': formData,
            'message': message,
        })
    else:
        return render(request, 'addBooks/addBooks.html', {
            'form': formData,
        })


def detailBook(request, id=None):
    return None


def changeBook():
    return None
