from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.pages, name="page"),
    path("create", views.create, name="create"),
    path("random", views.Random, name="random"),
    path("search", views.search, name="search"),
    path("edit/<str:title>", views.edit, name="edit")
]
