from django.conf.urls import url
from . import views

urlpatterns = [

    #初期表示
    url(r'^$', views.booklist_template, name='index'),
    #検索ボタン押下時表示
    url('^search/', views.index, name='search'),
    #全件検索ボタン押下時表示
    url('^allsearch/', views.allsearch, name='all'),

]
