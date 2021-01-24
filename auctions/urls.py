from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listingpage, name="listingpage"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path("removewatchlist<int:id>", views.removewatchlist, name="removewatchlist"),
    path("addcomment/<int:id>", views.addcomment, name = "addcomment"),
    path("addbid/<int:id>", views.addbid, name = "addbid"),
    path("closebid<int:id>", views.closebid, name = "closebid"),
    path("categories", views.categories, name = "categories"),
    path("category/<str:category>", views.category, name = "category")
]
