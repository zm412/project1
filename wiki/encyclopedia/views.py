from django.shortcuts import render
from django import forms
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

def arcticle(request, title):
    text = util.get_entry(title)
    md = markdown.Markdown()
    article = md.convert(text)

    if article:
        return render(request, 'encyclopedia/article.html', {
            "title": title,
            "article": article
        })
    else:
        return HttpResponse("Error")



