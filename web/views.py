from csv import reader
import re
# from mmap import mmap
from django.shortcuts import render
import simplejson
import urllib2
import wikipedia

from sas.settings import BASE_DIR


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
    data = getdata(eid, 1, 0)

    # grab keywords from data
    column = (1, 2, 3, 8, 12)
    keywords = ''
    for col in column:
        keywords += data[0][col] + ' '

    titles = wikipedia.search(keywords)

    page = wikipedia.page(titles[0])

    # get images from google using ajax from googleapis

    searchTerm = titles[0]

    img_urls = []

    searchTerm = searchTerm.replace(' ', '+')
    url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + searchTerm
    url_request = urllib2.Request(url, None)
    response = urllib2.urlopen(url_request)
    results = simplejson.load(response)
    content = results['responseData']
    dataInfo = content['results']
    for url in dataInfo:
        img_urls.append(url['unescapedUrl'])

    content = page.content
    re.sub('[\=]+([A-Za-z\ ])+[\=]+', '<h4>$1</h4><br>', content)

    return render(request, 'detail.html',
                  {'eid': eid, 'data': data[0], 'page': page, 'content': content, 'img_urls': img_urls})