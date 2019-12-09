from django import forms


class AddBookForm(forms.Form):
    isbn = forms.CharField(
        label='ISBN',
        required=True,
    )

    author = forms.CharField(
        label='著者',
        max_length=200,
        required=True,
        widget=forms.TextInput()
    )

    picture_name = forms.CharField(
        label='書影URL',
        max_length=200,
        required=True,
        widget=forms.TextInput()
    )

    title = forms.CharField(
        label='書名',
        max_length=200,
        required=True,
        widget=forms.TextInput()
    )

    publisher = forms.CharField(
        label='出版社',
        max_length=200,
        required=True,
        widget=forms.TextInput()
    )

    pubdate = forms.DateField(
        label='出版日',
        required=True,
        input_formats=[
            '%Y-%m-%d',  # 2010-01-01
            '%Y/%m/%d',  # 2010/01/01
            '%Y%m%d',    # 20100101
        ]
    )

    def __str__(self):
        return self.isbn
