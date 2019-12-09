from django.urls import path

from . import views

urlpatterns = [
    path('', views.newBook, name='newBook'),
]