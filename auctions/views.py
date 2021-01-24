from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, listing, Watchlist, Comment, Bid

class create_form(forms.Form):
    title = forms.CharField()
    description = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 15}))
    price = forms.IntegerField()
    category = forms.CharField()
    image = forms.URLField()

def categories(request):
    items=listing.objects.raw("SELECT * FROM auctions_listing GROUP BY category")
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/categories.html",{
        "items": items,
        "wcount":wcount
    })

def category(request,category):
    catitems = listing.objects.filter(category=category)
    try:
        w = Watchlist.objects.filter(user=request.user.username)
        wcount=len(w)
    except:
        wcount=None
    return render(request,"auctions/category.html",{
        "items":catitems,
        "cat":category,
        "wcount":wcount
    })

@login_required(login_url= 'login')
def closebid(request, id):
    item = listing.objects.get(id = id)
    item.active = False
    item.save()
    return redirect('listingpage', id = id)

@login_required(login_url= 'login')
def addbid(request, id):
    if request.method == "POST":
        cbid = listing.objects.get(id = id)
        cprice = cbid.price
        user_bid = int(request.POST.get('bid'))
        response =  redirect('listingpage', id = id)
        if user_bid > cprice:
            cbid.price = user_bid
            cbid.save()
            try:
                if Bid.objects.filter(listingid = id):
                    bidrow = Bid.objects.filter(listingid = id)
                    bidrow.delete()
                bidtable = Bid()
                bidtable.user=request.user.username
                bidtable.listingid = id
                bidtable.save()
            except:
                bidtable = Bid()
                bidtable.user=request.user.username
                bidtable.listingid = id
                bidtable.save()
            response.set_cookie('errorgreen','bid successful!!!',max_age=3)
        else:
            response.set_cookie('error','Bid should be greater than current price',max_age=3)
        return response

@login_required(login_url= 'login')
def addwatchlist(request, id):
    w = Watchlist()
    w.user = request.user.username
    w.listingid = id
    w.save()
    return redirect('listingpage', id = id)

@login_required(login_url= 'login')
def addcomment(request, id):
    if request.method == "POST":
        c = Comment()
        c.listingid = id
        c.user = request.user.username
        c.comment = request.POST.get('comment')
        c.save()
        return redirect('listingpage', id = id)

@login_required(login_url= 'login')
def removewatchlist(request, id):
    try:
        w = Watchlist.objects.get(user = request.user.username, listingid = id)
        w.delete()
        return redirect('listingpage', id = id)
    except:
        return redirect('listingpage', id = id)

@login_required(login_url= 'login')
def watchlist(request):
    w = Watchlist.objects.filter(user = request.user.username)
    items = []
    wcount = len(w)
    if wcount == 0:
        empty = True
    else:
        for item in w:
            items.append(listing.objects.get(id = item.listingid))
        empty = False
    return render(request, "auctions/watchlist.html", {
        "items":items, "wcount" :wcount, "empty":empty
    })
  
def index(request):
    items = listing.objects.all()
    w = Watchlist.objects.filter(user = request.user.username)
    wcount = len(w)
    return render(request, "auctions/index.html",{
        "items":items, "wcount":wcount
    })

@login_required(login_url= 'login')
def create(request):
    if request.method == 'POST':
        form = create_form(request.POST)
        if form.is_valid():
            listable = listing()
            listable.owner = request.user.username
            listable.title = form.cleaned_data["title"]
            listable.description = form.cleaned_data["description"]
            listable.price = form.cleaned_data["price"]
            listable.category = form.cleaned_data["category"]
            listable.image = form.cleaned_data["image"]
            listable.active = True
            listable.save()
        return redirect('index')
    else:
        form = create_form()
        return render(request, "auctions/create.html", {
            "form":form
        })

def listingpage(request, id):
    w = Watchlist.objects.filter(user = request.user.username)
    wcount = len(w)
    try:
        item = listing.objects.get(id = id)
    except:
        return redirect('index')
    if Watchlist.objects.filter(user = request.user.username, listingid = id):
        added = True
    else:
        added = False
    try:
        comments = Comment.objects.filter(listingid = id)
    except:
        comments = None
    if item.owner == request.user.username:
        owner = True
    else:
        owner = False
    try:
        buyer =  Bid.objects.get(listingid = id)
        buyer = buyer.user
    except:
         buyer = False
    return render(request, "auctions/listingpage.html", {
        "item":item, "added":added, "comments":comments,
        "error":request.COOKIES.get('error'),
        "errorgreen":request.COOKIES.get('errorgreen'),
        "wcount":wcount, "owner":owner, "active":item.active, "buyer":buyer
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
