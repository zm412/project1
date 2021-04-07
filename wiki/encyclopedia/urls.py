from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("add/", views.add, name="add"),
    path("random", views.random, name="random"),
    path("search/", views.search, name="search"),
    path("<str:title>/update/", views.update, name="update"),
    path("<str:title>/", views.article, name='article')
]
