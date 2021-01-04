from django.shortcuts import render, redirect
import markdown2
from django import forms
import random

from . import util


class search(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'search', 'placeholder': 'Search Encyclopedia'}))

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 15}))

def index(request):
    entries = util.list_entries()
    if request.method == "POST":
        items = []
        form = search(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            for entry in entries:
                if title.lower() == entry.lower():
                    page = util.get_entry(title)
                    html = markdown2.markdown(page)
                    return render(request, "encyclopedia/title.html", {
                        "title": title, "html": html
                    })
                if entry.lower().find(title.lower()) != -1:
                    items.append(entry)
            if not items:
                return render(request, "encyclopedia/index.html",{
                    "match":True, "form":form, "entries":entries
                })
            else:
                return render(request, "encyclopedia/search.html", {
                    "items": items
                })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries, "form": search(), "match":False
        })


def pages(request, title):
    page = util.get_entry(title)
    if page == None:
        return render (request, "encyclopedia/error.html")
    else:
        html = markdown2.markdown(page)
        return render(request, "encyclopedia/title.html", {
            "title": title, "html": html
        })


def create(request):
    if request.method == "POST":
        create_form = NewEntryForm(request.POST)
        entries = util.list_entries()
        if create_form.is_valid():
            if create_form.cleaned_data["title"].lower().capitalize() in entries:
                return render(request, "encyclopedia/create.html",{
                    "form1":create_form, "present":True
                })
            util.save_entry(create_form.cleaned_data["title"], create_form.cleaned_data["content"])
            return redirect(pages, title = create_form.cleaned_data["title"])   
    return render(request, "encyclopedia/create.html", {
        "form1":NewEntryForm(), "present":False
    })


def Random(request):
    entries = util.list_entries()
    title = random.choice(entries)
    page = util.get_entry(title)
    html = markdown2.markdown(page)
    return render(request, "encyclopedia/title.html", {
        "title": title, "html": html
    })

def edit(request, title):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
            return redirect(pages, title = form.cleaned_data["title"])
    if request.method == "GET":
        page = util.get_entry(title)
        details = {
            "title" : title,
            "content" : page
        }
        form = NewEntryForm(initial = details)
        return render(request, "encyclopedia/edit.html",{
            "form1" : form, "title":title
        })
        
