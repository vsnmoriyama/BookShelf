import sys
import threading

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseBadRequest

sys.path.append('../')
from bookList.models import book
from userManagement.models import User
from .models import BookStatus, BookReview
from . import form, getTestData


def newBook(request):
    try:
        request.session['userId']
    except KeyError:
        return redirect('userManagement:top')

    return render(request, 'addBooks/addBooks.html', {'book': book(), 'form': form.AddBookForm(), 'buttonName': 'add'})


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
            books.genre = request.POST['genre']
            books.text = request.POST['text']
            books.price = request.POST['price']

        else:
            books = book(isbn=request.POST['isbn'], picture_name=request.POST['picture_name'],
                         title=request.POST['title'], author=request.POST['author'],
                         publisher=request.POST['publisher'], pubdate=request.POST['pubdate'],
                         genre=request.POST['genre'], text=request.POST['text'], price=request.POST['price'])

        books.save()
        return redirect('addBooks:detailBook', isbn=isbnCode)
    else:
        retData = {'form': formData, }
        if request.POST['isbn']:
            retData['isbn'] = request.POST['isbn']
        return render(request, 'addBooks/addBooks.html', retData)


def detailBook(request, isbn=None, ):
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
    review = BookReview.objects.filter(isbn=isbn)
    users = User.objects.filter(user_id__in=[str(x.user_id) for x in review])
    userList = {}
    for user in users:
        userList[user.user_id] = user.user_name
    return render(request, 'addBooks/detail.html',
                  {'book': books, 'cCode': changeCCode(books.genre),
                   'getBookForm': form.GetBookForm(request.POST or None, initial=initials),
                   'bookReviewForm': form.BookReviewForm(request.POST or None, initial={'isbn': isbn}),
                   'reviews': review, 'users': userList, 'reviewCount': len(review)})


def changeBook(request, isbn=None):
    try:
        request.session['userId']
    except KeyError:
        return redirect('userManagement:top')
    books = get_object_or_404(book, isbn=isbn)
    formData = form.AddBookForm(
        initial={'isbn': books.isbn, 'picture_name': books.picture_name, 'title': books.title, 'author': books.author,
                 'publisher': books.publisher, 'pubdate': books.pubdate, 'genre': books.genre, 'text': books.text,
                 'price': books.price})

    return render(request, 'addBooks/addBooks.html', {'form': formData, 'isbn': isbn, 'buttonName': 'change'})


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
        reviewData = BookReview(user_id=userId, isbn=isbn, star=star, review=review)
        reviewData.save()
        return HttpResponse()
    except KeyError:
        return HttpResponseBadRequest()


def changeCCode(c_code):
    hanbai = {'0': '一般', '1': '教養', '2': '実用', '3': '専門', '5': '婦人', '6': '学参I(小中)', '7': '学参II(高校)', '8': '児童',
              '9': '雑誌扱い', }
    hakkou = {'0': '単行本', '1': '文庫', '2': '新書', '3': '全集・双書', '4': 'ムック・その他', '5': '事書・辞典', '6': '図鑑', '7': '絵本',
              '8': '磁性媒体など', '9': 'コミック', }
    naiyo = {'00': '総記', '01': '百科事典', '02': '年鑑・雑誌', '04': '情報科学', '10': '哲学', '11': '心理(学)', '12': '倫理(学)',
             '14': '宗教', '15': '仏教', '16': 'キリスト教', '20': '歴史総記', '21': '日本歴史', '22': '外国歴史', '23': '伝記', '25': '地理',
             '26': '旅行', '30': '社会科学総記', '31': '政治-含む国防軍事', '32': '法律', '33': '経済・財政・統計', '34': '経営', '36': '社会',
             '37': '教育', '39': '民族・風習', '40': '自然科学総記', '41': '数学', '42': '物理学', '43': '化学', '44': '天文・地学', '45': '生物学',
             '47': '医学・歯学・薬学', '50': '工学・工学総記', '51': '土木', '52': '建築', '53': '機械', '54': '電気', '55': '電子通信',
             '56': '海事', '57': '採鉱・冶金', '58': 'その他の工業', '60': '産業総記', '61': '農林業', '62': '水産業', '63': '商業',
             '65': '交通・通信', '70': '芸術総記', '71': '絵画・彫刻', '72': '写真・工芸', '73': '音楽・舞踊', '74': '演劇・映画', '75': '体育・スポーツ',
             '76': '諸芸・娯楽', '77': '家事', '79': 'コミックス・劇画', '80': '語学総記', '81': '日本語', '82': '英米語', '84': 'ドイツ語',
             '85': 'フランス語', '87': '各国語', '90': '文学総記', '91': '日本文学総記', '92': '日本文学詩歌', '93': '日本文学、小説・物語',
             '95': '日本文学、評論、随筆、その他', '97': '外国文学小説', '98': '外国文学、その他'}
    if c_code and len(c_code) == 4:
        hanbaiData = hanbai[c_code[:1]]
        hakkouData = hakkou[c_code[1:2]]
        naiyoData = naiyo[c_code[2:4]]
        return {'hanbai': hanbaiData, 'hakkou': hakkouData, 'naiyo': naiyoData}
    else:
        return None


def getRandom(request):
    thread_1 = threading.Thread(target=getTestData.createData())
    thread_1.start()
    return HttpResponse()
