from django.urls import path

from . import views

urlpatterns = [
    path('', views.newBook, name='newBook'),
    path('getRandom', views.getRandom, name='getRandom'),
    path('add', views.addBook, name='addBook'),
    path('<int:isbn>/', views.detailBook, name='detailBook'),
    path('<int:isbn>/change', views.changeBook, name='changeBook'),
    path('addStatus', views.addStatus, name='addStatus'),
    path('addReview', views.addReview, name='addReview'),
]
