import mmap
import os
from django.shortcuts import render
from sas.settings import BASE_DIR


def index(request):
    return render(request, 'index.html')


def search(request):
    if request.method == 'GET':
        return render(request, 'search.html')
    query = request.POST.get('query', '')
    # collect data from CSV and list it
    # read CSV with filter
    data = list()
    with open(os.path.join(BASE_DIR,  '/media/globalterrorismdb_0814dist.csv'), 'r+b') as f:
    # with open('/Users/SmAaMyA/Documents/PyCharm/guinw/media/globalterrorismdb_0814dist.csv', 'r+b') as f:
        # memory-mapInput the file, size 0 means whole file
        map_input = mmap.mmap(f.fileno(), 0)
        # read content via standard file methods
        for s in iter(map_input.readline, ""):
            if s.find(query) != -1:
                data.append(s)
        map_input.close()
    f.close()
    # return data
    return render(request, 'search.html', {'query': query, 'data': data})


def detail(request, eid):
    # gathering information from wikipedia and get images from sources
    return render(request, 'detail.html', {'eid': eid})