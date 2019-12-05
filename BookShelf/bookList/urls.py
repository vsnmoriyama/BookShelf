from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.booklist_template, name='index'),
]
