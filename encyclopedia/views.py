from django.shortcuts import render, redirect
from django.http import HttpResponse
import markdown
from django import forms
import random
from random import choice
from . import util


class searchform(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'search', 'placeholder':'Search Encyclopedia', 'placeholder':'Search Encyclopedia'})) 
class createform(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder':'Title'})) 
    entry = forms.CharField(label="", widget=forms.Textarea(attrs={'cols': '15'}))
class editform(forms.Form):
    entry = forms.CharField(label="", widget=forms.Textarea(attrs={'cols': '15'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchform()
    })

def page(request, name):
    if util.get_entry(name) != None:
        return render(request, "encyclopedia/entry.html", {
        "entry": markdown.markdown(util.get_entry(name)),
        "name": name
        })
    else:
        return render(request, "encyclopedia/noentry.html")

def wiki(request):
    response = redirect('/')
    return response

def editroot(request):
    response = redirect('/')
    return response

input1 = None

def search(request):

    if request.method == "POST":

        form = searchform(request.POST)
        if form.is_valid():
            
            input = form.cleaned_data["search"]
            input1 = str(input)
            entries = util.list_entries()
            for entry in entries:
                if input.lower() == str(entry).lower():
                    response = redirect('wiki/' + input)
                    return response
            entries = util.list_entries()
            foundentries = []
            for entry in entries:
                if input.lower() in str(entry).lower():
                    foundentries.append(entry)
            if len(foundentries) != 0:
                return render(request, "encyclopedia/results.html", {
                "input": input1,
                "entries": foundentries
                })


            return render(request, "encyclopedia/noresults.html", {
            "input": input1
            })
    else:
        response = redirect('/')
        return response

def create(request):
    if request.method == "POST":
        form = createform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]
            for entry1 in util.list_entries():
                if entry1.lower() == title.lower():
                    return render(request, "encyclopedia/create.html",{
                        "error": "This entry already exists!"
                    })
            util.save_entry(title, entry)
            response = redirect('/wiki/'+ title)
            return response
    else:
        return render(request, "encyclopedia/create.html")
    
def edit(request, name):
    if request.method == "POST":
        form = editform(request.POST)
        print(form)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            util.save_entry(name, entry)
            response = redirect('/wiki/'+ name)
            return response
    else:
        return render(request, "encyclopedia/edit.html", {
            "entrytext": util.get_entry(name),
            "name": name
        })

def random(request):
    entries = util.list_entries()
    randomentry = choice(entries)
    response = redirect('/wiki/' + randomentry)
    return response