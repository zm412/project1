from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from random import randint
import re
#import markdown

from . import util

class NewItemCreate(forms.Form):
    title = forms.CharField()
    article = forms.CharField(widget=forms.Textarea)

class SearchArticle(forms.Form):
    q = forms.CharField(label = '')

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
            if  not util.get_entry(title):
                content = newArticle.cleaned_data['article']
                full_article = '#' + title + '\n' + content
                print (full_article)
                util.save_entry(title, full_article)
                return render(request, 'encyclopedia/add.html', {
                    "form": NewItemCreate(),
                    "comment": "Article added",
                    "title": title
                })
            else:
                return render(request, 'encyclopedia/add.html', {
                    "form": NewItemCreate(),
                    "comment": "Sorry, article with this title already exists",
                    "title": title
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
    list_arts = util.list_entries()
    length = len(list_arts)
    random_num = randint(0, length - 1)
    random_title = list_arts[random_num]
    return redirect(random_title+'/')


def article(request, title):
    text = util.get_entry(title)
    if text:
       #md = markdown.Markdown()
       #article = mark_safe(md.convert(text))
       article = mark_safe(convertToHTML(text))
       return render(request, 'encyclopedia/article.html', {
            "title":title,
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



def update(request, title):
    article = util.get_entry(title)
    f = NewItemCreate(initial={"title": title, "article": article})
    if request.method == 'POST':
        updated_form = NewItemCreate(request.POST)
        if(updated_form.is_valid()):
            if util.get_entry(title):
                content = updated_form.cleaned_data['article']
                util.save_entry(title, content)
                updated_article = util.get_entry(title)
                return redirect('../')
            else:
                return render(request, 'encyclopedia/update.html', {
                        "comment": "If you want to create new article, please use option 'Add article'",
                        "title": title
                    })
        else:
            return render(request, 'encyclopedia/update.html', {
                    "form": f,
                    "comment": "Data is not valid",
                    "title": title
                })

    else :
        return render(request, 'encyclopedia/update.html', {
                "form": f,
            })

def filter_list(listN, title):
    outList = []
    for s in listN:
        elemLow = s.lower()
        titleLow = title.lower()
        if(elemLow.find(titleLow) != -1):
            outList.append(s)
    return  outList

def convertToHTML(text):
    print(text)
    n = re.sub(r'\#(.+[^\n])', r'<h1>\1</h1>', text)
    n = re.sub(r'(?<=[^\*{2,}])\*\s([^\n]+)', r'<li>\1</li>', n)
    n = re.sub(r'\*{2}([^\n]+?)\*{2}', r'<strong>\1</strong>', n)
    n = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', n)
    return n














