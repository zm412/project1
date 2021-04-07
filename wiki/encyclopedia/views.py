from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from random import randint
import re

from . import util

class NewItemCreate(forms.Form):
    title = forms.CharField()
    article = forms.CharField(widget=forms.Textarea)

class UpdateArticle(forms.Form):
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
            content = newArticle.cleaned_data['article']
            if  not util.get_entry(title):
                full_article = '# ' + title + '\n' + content
                util.save_entry(title, full_article)
                return render(request, 'encyclopedia/add.html', {
                    "form": NewItemCreate(),
                    "comment": "Article added",
                    "title": title,
                    "style": 'color: green; font-weight: bold'
                })
            else:
                return render(request, 'encyclopedia/add.html', {
                    "exist_data": title,
                    "comment": "Article with this title already exists",
                    "form": NewItemCreate(initial={"title": title, "article": content }),
                    "title": title,
                    "style": 'color: red; font-weight: bold'
                })
        else:
            return render(request, 'encyclopedia/add.html', {
                "form": NewItemCreate(),
                "comment": "not valid",
                "style": 'color: red; font-weight: bold'
            })
    else:
        return render(request, 'encyclopedia/add.html', {
            "form": NewItemCreate(),
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
    f = UpdateArticle(initial={"article": article})
    if request.method == 'POST':
        updated_form = UpdateArticle(request.POST)
        if(updated_form.is_valid()):
            if util.get_entry(title):
                content = updated_form.cleaned_data['article']
                if  content.find('#'+ title) != -1:
                    util.save_entry(title, content)
                    updated_article = util.get_entry(title)
                    return redirect('../')
                else:
                    return render(request, 'encyclopedia/update.html', {
                            "comment": "Name and #title of article must match!",
                            "title": title,
                            "style": 'color: red; font-weight: bold',
                            "form": UpdateArticle(initial={
                                "article": content})
                            })
            else:
                return render(request, 'encyclopedia/update.html', {
                        "comment": "If you want to create new article, please use option 'Add article'",
                        "style": 'color: red; font-weight: bold',
                        "title": title
                    })
        else:
            return render(request, 'encyclopedia/update.html', {
                    "form": f,
                    "comment": "Data is not valid",
                    "style": 'color: red; font-weight: bold',
                    "title": title
                })
    else :
        return render(request, 'encyclopedia/update.html', {
                "form": f,
                "title": title
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
    n = re.sub(r'\##(.+[^\n])', r'<h2>\1</h2>', text)
    n = re.sub(r'\#(.+[^\n])', r'<h1>\1</h1>', n)
    n = re.sub(r'(?<=[^\*{2,}])[\*|\-|\+]\s([^\n]+)', r'<li>\1</li>', n)
    n = re.sub(r'\*{2}([^\n]+?)\*{2}', r'<strong>\1</strong>', n)
    n = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', n)
    n = re.sub(r'\t{2}([^\n]+?)\t', r'<p>\1</p>', n)
    return n














