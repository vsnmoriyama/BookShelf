from django.urls import path

from . import views

urlpatterns = [
    path('', views.topPage, name='top'),
    path('menu/', views.menu, name='menu'),
]