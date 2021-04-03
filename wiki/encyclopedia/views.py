from django.shortcuts import render
from django import forms
from django.utils.safestring import mark_safe
import markdown

from . import util

class newItemCreate(forms.Form):
    title = forms.CharField()
    article = forms.CharField()




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def add(request):
    if request.method == 'POST':
        newArticle = newItemCreate(request.POST)
        print(newArticle, 'print')
        title = newArticle.cleaned_data['title']
        content = newArticle.cleaned_data['article']
        util.save_entry(title, content)
        return render(request, 'encyclopedia/index.html', {
            "entries": util.list_entries()
        })
    else:
        return render(request, 'encyclopedia/add.html', {
            "form": newItemCreate()
        })

def random(request):
    return render(request, "encyclopedia/random.html", {
        "entries": util.list_entries()
    })


def article(request, title):
    text = util.get_entry(title)
    md = markdown.Markdown()
    article = mark_safe(md.convert(text))
    print(text)
    print(article)

    if article:
        return render(request, 'encyclopedia/article.html', {
            "article": article
        })
    else:
        return HttpResponse("Error")






















