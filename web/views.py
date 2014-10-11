from mmap import mmap

import wikipedia
from django.shortcuts import render

from sas.settings import BASE_DIR


def index(request):
    return render(request, 'index.html')


def search(request, line=10, page=0):
    query = request.GET.get('query', '')
    # collect data from CSV and list it
    # read CSV with filter
    data = list()

    with open((BASE_DIR + '/media/globalterrorismdb_0814dist.csv'), 'r+b') as f:
        # memory-mapInput the file, size 0 means whole file
        map_input = mmap(f.fileno(), 0)
        # read content via standard file methods
        for s in iter(map_input.readline, ""):
            s = s.decode('latin-1')
            if s.find(query) != -1:
                data.append(s.split(','))
        map_input.close()
    f.close()

    data = data[::-1]
    data = data[line * page:line * page + line]

    # return data
    return render(request, 'search.html', {'query': query, 'data': data})


def detail(request, eid):
    # gathering information from wikipedia and get images from sources
    # from eid get keyword from csv
    summary = wikipedia.summary("9-11")
    return render(request, 'detail.html', {'eid': eid, 'summary': summary})