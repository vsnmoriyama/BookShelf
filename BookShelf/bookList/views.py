from django.http import HttpResponse
from django.shortcuts import render # 追加する
from .models import book  # 追加する

def booklist_template(request):
    d = {
        'books': book.objects.all(),
    }
    return render(request, 'bookList/index.html',d)
