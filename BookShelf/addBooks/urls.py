from django.urls import path

from . import views

urlpatterns = [
    path('', views.newBook, name='newBook'),
    path('add', views.addBook, name='addBook'),
    path('<int:isbn>/', views.detailBook, name='detailBook'),
    path('<int:isbn>/change', views.changeBook, name='changeBook'),
]
