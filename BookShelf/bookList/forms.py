from django import forms

class BookSearchForm(forms.Form):                                      #検索フォーム

    isbn = forms.CharField(label = 'ISBN', required=False)             #isbn
    picture_name = forms.CharField(label = '表紙', required=False)     #表紙
    title = forms.CharField(label = '書名', required=False)            #書名
    author = forms.CharField(label = '著者名', required=False)         #著者名
    publisher = forms.CharField(label = '出版社', required=False)      #出版社
    pubdate = forms.DateField(label = '出版日', required=False)        #出版日

#フォームに入力された値を取り出す
BookSearchFormSet = forms.formset_factory(BookSearchForm, extra=6)