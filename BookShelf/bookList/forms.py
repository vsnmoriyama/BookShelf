from django import forms

class BookSearchForm(forms.Form):

    isbn = forms.CharField(label = 'isbn', required=False)
    picture_name = forms.CharField(label = 'picture_name', required=False)
    title = forms.CharField(label = 'title', required=False)
    author = forms.CharField(label = 'author', required=False)
    publisher = forms.CharField(label = 'publisher', required=False)
    pubdate = forms.DateField(label = 'pubdate', required=False)

BookSearchFormSet = forms.formset_factory(BookSearchForm, extra=6)