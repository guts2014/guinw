from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def search(request):
    if request.method == 'GET':
        return render(request, 'search.html')


def detail(request, eid):
    return render(request, 'detail.html', {'eid': eid})