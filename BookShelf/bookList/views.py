from django.http import HttpResponse
from .models import book
from . import forms
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect


# 初期表示
def booklist_template(request):
    d = {

        # 'books': book.objects.all(),
        "bookSearchForm": forms.BookSearchForm()
    }
    return render(request, 'bookList/index.html', d)


# 検索ボタン押下時表示
def index(request):
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

    # [isbn]Query生成
    if request.GET['isbn']:
        isbnQuery = Q(isbn=request.GET['isbn'])

    # [title]Query生成
    if request.GET['title']:
        titleQuery = Q(title=request.GET['title'])

    # [auther]Query生成
    if request.GET['author']:
        authorQuery = Q(author=request.GET['author'])

    # [publisher]Query生成
    if request.GET['publisher']:
        publisherQuery = Q(publisher=request.GET['publisher'])

    # [pubdate]Query生成
    if request.GET['pubdate']:
        pubdateQuery = Q(pubdate=request.GET['pubdate'])

    # すべての検索フォームに値が入力されていない場合
    if (isbnQuery == Q() and
            titleQuery == Q() and
            authorQuery == Q() and
            publisherQuery == Q() and
            pubdateQuery == Q()
    ):
        # フォームデータのみ返却する値に代入する
        # 検索結果を0件とする
        d = {"bookSearchForm": formData}

    # 1つ以上の検索フォームに値が入力されている場合
    else:
        # 値の取得
        result = book.objects.filter(isbnQuery & titleQuery & authorQuery & publisherQuery & pubdateQuery)

        # フォームデータ、検索結果を返却する値に代入する
        d = {"books": result, "bookSearchForm": formData}

    return render(request, 'bookList/index.html', d)


# 全件検索ボタン押下時表示
def allsearch(request):
    d = {

        'books': book.objects.all(),
        "bookSearchForm": forms.BookSearchForm()

    }

    return render(request, 'bookList/index.html', d)
