import sys
import threading

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest

sys.path.append('../')
from bookList.models import book

from .models import BookStatus, BookReview
from . import form, getTestData


def newBook(request):
    try:
        request.session['userId']
    except KeyError:
        return redirect('userManagement:top')

    return render(request, 'addBooks/addBooks.html', {'book': book(), 'form': form.AddBookForm()})


def addBook(request):
    try:
        request.session['userId']
    except KeyError:
        return redirect('userManagement:top')
    # formの取得
    formData = form.AddBookForm(request.POST or None)
    if formData.is_valid():  # 入力チェック
        isbnCode = request.POST['isbn']
        books = book.objects.filter(isbn=isbnCode)
        if books.exists():
            books = books[0]
            books.picture_name = request.POST['picture_name']
            books.title = request.POST['title']
            books.author = request.POST['author']
            books.publisher = request.POST['publisher']
            books.pubdate = request.POST['pubdate']

        else:
            books = book(isbn=request.POST['isbn'], picture_name=request.POST['picture_name'],
                         title=request.POST['title'], author=request.POST['author'],
                         publisher=request.POST['publisher'], pubdate=request.POST['pubdate'])

        books.save()
        return redirect('addBooks:detailBook', isbn=isbnCode)
    else:
        return render(request, 'addBooks/addBooks.html', {
            'form': formData,
        })


def detailBook(request, isbn=None):
    try:
        userId = request.session['userId']
    except KeyError:
        return redirect('userManagement:top')
    books = get_object_or_404(book, isbn=isbn)
    bookStatus = BookStatus.objects.filter(isbn=isbn, user_id=userId)
    initials = {'isbn': isbn}
    if bookStatus.exists():
        initials['status'] = bookStatus[0].status
    else:
        initials['status'] = 'lost'
    return render(request, 'addBooks/detail.html',
                  {'book': books, 'getBookForm': form.GetBookForm(request.POST or None, initial=initials),
                   'bookReviewForm': form.BookReviewForm()})


def changeBook(request, isbn=None):
    try:
        request.session['userId']
    except KeyError:
        return redirect('userManagement:top')
    books = get_object_or_404(book, isbn=isbn)
    formData = form.AddBookForm(
        initial={'isbn': books.isbn, 'picture_name': books.picture_name, 'title': books.title, 'author': books.author,
                 'publisher': books.publisher, 'pubdate': books.pubdate})

    return render(request, 'addBooks/addBooks.html', {'form': formData, })


def addStatus(request):
    try:
        userId = request.session['userId']
        isbn = request.POST['isbn']
        status = request.POST['status']
    except KeyError:
        return HttpResponseBadRequest()
    if status == 'none':
        return HttpResponseBadRequest()
    bookStatus = BookStatus.objects.filter(isbn=isbn, user_id=userId)
    if bookStatus.exists():
        bookStatus = bookStatus[0]
        if status == 'lost':
            bookStatus.delete()
        else:
            bookStatus.status = status
            bookStatus.save()
    else:
        bookStatus = BookStatus(isbn=isbn, user_id=userId, status=status)
        bookStatus.save()
    return HttpResponse()


def addReview(request):
    try:
        userId = request.session['userId']
        isbn = request.POST['isbn']
        get_object_or_404(BookStatus, isbn=isbn, user_id=userId)

        star = request.POST['star']
        review = request.POST['review']
        review = review.replace('\r\n', '<br>')
        review = review.replace('\n', '<br>')
        review = review.replace('\r', '<br>')
        reviewData = BookReview(userId=userId, isbn=isbn, star=star, review=review)
        reviewData.save()
        return HttpResponse()
    except KeyError:
        return HttpResponseBadRequest()


def getRandom(request):
    thread_1 = threading.Thread(target=getTestData.createData())
    thread_1.start()
    return HttpResponse()
