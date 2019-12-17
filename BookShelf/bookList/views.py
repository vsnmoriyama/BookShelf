import sys
from .models import book
from . import forms
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
sys.path.append('../')
from addBooks.models import BookStatus

# 初期表示
def booklist_template(request):

    # キーの有無を調べる
    try:
        request.session['userId']
    except KeyError:
        return redirect('userManagement:top')

    d = {
            # 'books': book.objects.all(),
            "bookSearchForm": forms.BookSearchForm()
    }

    return render(request, 'bookList/index.html', d)


# 検索ボタン押下時表示
def index(request):

    try:
        userId=request.session['userId']
    except KeyError:
        return redirect('userManagement:top')
    # フォームデータの取得
    formData = forms.BookSearchForm(request.GET or None)

    # 取得するフォームデータ一覧
    # isbn [isbn]
    # 書名 [title]
    # 著者名 [author]
    # 出版社 [publisher]
    # 出版日 [pubdate]

    # Query生成
    # 初期化
    isbnQuery = Q()
    titleQuery = Q()
    authorQuery = Q()
    publisherQuery = Q()
    pubdateQuery = Q()
    statusQuery = Q()

    # [isbn]Query生成
    if 'isbn' in request.GET and request.GET['isbn']:
        isbnQuery = Q(isbn=request.GET['isbn'])
    # [title]Query生成
    if 'title' in request.GET and request.GET['title']:
        titleQuery = Q(title=request.GET['title'])
    # [author]Query生成
    if 'author' in request.GET and request.GET['author']:
        authorQuery = Q(author=request.GET['author'])
    # [publisher]Query生成
    if 'publisher' in request.GET and request.GET['publisher']:
        publisherQuery = Q(publisher=request.GET['publisher'])
    # [pubdate]Query生成
    if 'pubdate' in request.GET and request.GET['pubdate']:
        pubdateQuery = Q(pubdate=request.GET['pubdate'])
    # [status]Query生成
    if 'status' in request.GET and request.GET['status'] and not 'none' == request.GET['status']:
        statusList=BookStatus.objects.values_list('isbn', flat=True).filter(user_id=userId, status=request.GET['status'])
        statusQuery = Q(isbn__in=statusList)

    # すべての検索フォームに値が入力されていない場合
    if (isbnQuery == Q() and
        titleQuery == Q() and
        authorQuery == Q() and
        publisherQuery == Q() and
        pubdateQuery == Q() and
        statusQuery == Q()
        ):

        series = book.objects.all().order_by('id')
        page_obj = paginate_query(request, series, 10)  # ページネーション

        d = {

            # モデルから取得したobjectsの代わりに、page_objを渡す
            'page_obj': page_obj,
            'site_name': "",
            "bookSearchForm": forms.BookSearchForm()

        }

    # 1つ以上の検索フォームに値が入力されている場合
    else:
        # 値の取得
        #result = book.objects.filter(isbnQuery & titleQuery & authorQuery & publisherQuery & pubdateQuery)
        series = book.objects.filter(isbnQuery & titleQuery & authorQuery & publisherQuery & pubdateQuery & statusQuery).order_by('id')
        page_obj = paginate_query(request, series, 10)  # ページネーション

        # フォームデータ、検索結果を返却する値に代入する
        d = {"page_obj": page_obj, "bookSearchForm": formData}

    return render(request, 'bookList/index.html', d)


# 全件検索ボタン押下時表示
def allsearch(request):

    # キーの有無を調べる
    try:
        request.session['userId']
    except KeyError:
        return redirect('userManagement:top')

    d = {

        "bookSearchForm": forms.BookSearchForm()

        }

    return render(request, 'bookList/index.html', d)


# ページネーション用に、Pageオブジェクトを返す。
def paginate_query(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj
