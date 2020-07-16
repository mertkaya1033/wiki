from django.shortcuts import render
from markdown2 import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry_file = util.get_entry(title)

    if entry_file is not None:
        try:
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entryData": markdown(entry_file)
            })
        except Exception:
            return render(request, "encyclopedia/error.html", {
                "errorMessage": "Markdown entry is not readable"
            })

    return render(request, "encyclopedia/error.html", {
        "errorMessage": f"No such entry with title \"{title}\""
    })


def search(request):
    if request.method == "POST" and "q" in request.POST:
        query = request.POST["q"]
        entries = util.list_entries()
        context = {
            "search": query,
            "results": []
        }
        for entry_title in entries:
            if query.lower() == entry_title.lower():
                return HttpResponseRedirect(
                    reverse("entry", args=(entry_title,)))
            if query.lower() in entry_title.lower():
                context["results"].append(entry_title)
        return render(request, "encyclopedia/search_results.html", context)

    return HttpResponseRedirect(reverse("index"))
