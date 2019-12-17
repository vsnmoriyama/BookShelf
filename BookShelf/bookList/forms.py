from django import forms
import sys

sys.path.append('../')
from addBooks.form import GetBookForm


class BookSearchForm(forms.Form):                                      #検索フォーム

    isbn = forms.CharField(label = 'ISBN', required=False)             #isbn
    title = forms.CharField(label = '書名', required=False)            #書名
    author = forms.CharField(label = '著者名', required=False)         #著者名
    publisher = forms.CharField(label = '出版社', required=False)      #出版社
    pubdate = forms.DateField(label = '出版日', required=False)        #出版日
    status = forms.ChoiceField(label = 'ステータス', required=False,choices=GetBookForm.BOOK_STATUS)        #所持ステータス

#フォームに入力された値を取り出す
BookSearchFormSet = forms.formset_factory(BookSearchForm, extra=6)