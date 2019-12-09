import sys, threading

from django.shortcuts import render, get_object_or_404

sys.path.append('../')
from bookList.models import book

from . import form, getTestData


def newBook(request):
    thread_1 = threading.Thread(target=getTestData.createData())
    thread_1.start()
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
            books.author = request.POST['author']
            books.publisher = request.POST['publisher']
            books.pubdate = request.POST['pubdate']
            message = 'update Book'

        else:

            books = book(isbn=request.POST['isbn'], picture_name=request.POST['picture_name'],
                         title=request.POST['title'], author=request.POST['author'],
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


def detailBook(request, isbn=None):
    books = get_object_or_404(book, isbn=isbn)
    return render(request, 'addBooks/detail.html', {'book': books})


def changeBook(request, isbn=None):
    books = get_object_or_404(book, isbn=isbn)
    formData = form.AddBookForm(
        initial={'isbn': books.isbn, 'picture_name': books.picture_name, 'title': books.title, 'auther': books.auther,
                 'publisher': books.publisher, 'pubdate': books.pubdate})

    return render(request, 'addBooks/addBooks.html', {'form': formData, })
