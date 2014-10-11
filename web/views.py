from csv import reader
from django.shortcuts import render
# from mmap import mmap
from django.shortcuts import render
from sas.settings import BASE_DIR
import simplejson
import urllib2
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

    with open(BASE_DIR + '/media/globalterrorismdb_0814dist.csv', 'rb') as csv_file:
        row_reader = reader(csv_file, delimiter=',', quotechar='"')
        for row in row_reader:
            if query in row:
                data.append(row)
    csv_file.close()

    # with open((BASE_DIR + '/media/globalterrorismdb_0814dist.csv'), 'r+b') as f:
    #     # memory-mapInput the file, size 0 means whole file
    #     map_input = mmap(f.fileno(), 0)
    #     # read content via standard file methods
    #     for s in iter(map_input.readline, ''):
    #         s = s.decode('latin-1')
    #         if s.find(query) != -1:
    #             data.append(s.split(','))
    #     map_input.close()
    # f.close()

    # sort by date, most recent event come first
    data.reverse()
    # partitioning elements to show in one page
    data = data[line * page:line * page + line]

    return data


def search(request, line=10, page=1):
    query = request.GET.get('query', '')
    line = int(line)
    page = int(page)
    return render(request, 'search.html', {'query': query, 'data': getdata(query, line, page - 1), 'page': page})


def detail(request, eid):
    # gathering information from wikipedia and get images from sources
    # from eid get keyword from csv
    data = getdata(eid, 1, 0)

    # grab keywords from data
    column = (1, 2, 3, 8, 12)
    keywords = ''
    for col in column:
        keywords += data[0][col] + ' '

    titles = wikipedia.search(keywords)
    print titles
    # print wikipedia.page(titles)

    summary = wikipedia.summary("9-11")
    return render(request, 'detail.html', {'eid': eid, 'summary': summary})