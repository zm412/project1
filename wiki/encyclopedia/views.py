from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import markdown

from . import util

class NewItemCreate(forms.Form):
    title = forms.CharField()
    article = forms.CharField(widget=forms.Textarea)


class SearchArticle(forms.Form):
    q = forms.CharField(label='')



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchArticle()
    })

def add(request):
    if request.method == 'POST':
        newArticle = NewItemCreate(request.POST)
        if newArticle.is_valid():
            title = newArticle.cleaned_data['title']
            content = newArticle.cleaned_data['article']
            util.save_entry(title, content)
            return render(request, 'encyclopedia/add.html', {
                "form": NewItemCreate(),
                "comment": "Article added"
            })
        else:
            return render(request, 'encyclopedia/add.html', {
                "form": NewItemCreate(),
                "comment": "not valid"
            })
    else:
        return render(request, 'encyclopedia/add.html', {
            "form": NewItemCreate(),
            "comment": "add new?"
        })

def random(request):
    return render(request, "encyclopedia/random.html", {
        "entries": util.list_entries()
    })


def article(request, title):
    text = util.get_entry(title)
    if text:
        md = markdown.Markdown()
        article = mark_safe(md.convert(text))
        return render(request, 'encyclopedia/article.html', {
            "article": article
        })
    else:
        return render(request, 'encyclopedia/article.html', {
            "article": 'Wiki does not have an arcticle with this name'
        })


def search(request):
    if request.method == 'POST':
        form_data = SearchArticle(request.POST)
        if form_data.is_valid():
            title = form_data.cleaned_data['q']
            text = util.get_entry(title)
            if text:
                return redirect('../'+title+'/')
            else:
                list_n = util.list_entries()
                print(list_n)
                filtered_list = filter_list(list_n, title)
                return render(request, 'encyclopedia/search.html', {
                    "filtered" : filtered_list
                })
        else:
            return render(request, 'encyclopedia/index.html')
    else:
        return render(request, 'encyclopedia/index.html')


def filter_list(listN, title):
    outList = []
    for s in listN:
        elemLow = s.lower()
        titleLow = title.lower()
        if(elemLow.find(titleLow) != -1):
            outList.append(s)
    return  outList


















