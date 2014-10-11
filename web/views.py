from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def search(request):
    if request.method == 'GET':
        return render(request, 'search.html')
    query = request.POST.get('query', '')
    # collect data from CSV and list it
    # read CSV with filter
    data = []
    # return data
    return render(request, 'search.html', {'query': query, 'data': data})


def detail(request, eid):
    # gathering information from wikipedia and get images from sources
    return render(request, 'detail.html', {'eid': eid})