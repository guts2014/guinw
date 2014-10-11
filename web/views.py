from django.shortcuts import render
from mmap import mmap
import urllib2

from django.shortcuts import render
import simplejson
import wikipedia


MONTH = {1: 'January',
         2: 'February',
         3: 'March',
         4: 'April',
         5: 'May',
         6: 'June',
         7: 'July',
         8: 'August',
         9: 'September',
         10: 'October',
         11: 'November',
         12: 'December'}


def index(request):
    return render(request, 'index.html')


def getdata(query, line, page):
    # collect data from CSV and list it
    # read CSV with filter
    data = list()
    with open((BASE_DIR + '/media/globalterrorismdb_0814dist.csv'), 'r+b') as f:
        # memory-mapInput the file, size 0 means whole file
        map_input = mmap(f.fileno(), 0)
        # read content via standard file methods
        for s in iter(map_input.readline, ''):
            s = s.decode('latin-1')
            if s.find(query) != -1:
                data.append(s.split(','))
        map_input.close()
    f.close()

    data = data[::-1]
    data = data[line * page:line * page + line]

    # return data
    return data


def search(request, line=10, page=1):
    query = request.GET.get('query', '')
    line = int(line)
    page = int(page)
    return render(request, 'search.html', {'query': query, 'data': getdata(query, line, page - 1), 'page': page})


def detail(request, eid):
    # gathering information from wikipedia and get images from sources
    # from eid get keyword from csv

    # re-use getdata() method to look for keywords
    data = getdata(eid, 10, 0)
    print eid
    print data

    titles = wikipedia.search('2009 September 28  Myanmar Kokang')
    a = wikipedia.page(titles)
    a.content
    print titles

    summary = wikipedia.summary("9-11")
    return render(request, 'detail.html', {'eid': eid, 'summary': summary})