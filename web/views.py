from csv import reader
from sas.settings import BASE_DIR

from django.shortcuts import render
import re
import simplejson
import urllib2
import wikipedia


__MONTH__ = {1: 'January',
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


__TR_RECORDS__ = list()
__DUMMY_RECORDS__ = list()
with open(BASE_DIR + '/media/globalterrorismdb_0814dist.csv', 'rb') as csv_file:
    row_reader = reader(csv_file, delimiter=',', quotechar='"')
    for row in row_reader:
        __TR_RECORDS__.append(row)
        __DUMMY_RECORDS__.append(list(s.lower() for s in row))
csv_file.close()
# sort data from the most recent event
__TR_RECORDS__.reverse()
__DUMMY_RECORDS__.reverse()


def index(request):
    return render(request, 'index.html')


def get_data(query, line, page):
    # convert query to lowercase to search by non-case sensitive
    query = unicode(query).lower()

    data = list()
    size = line * page
    page -= 1
    l = 0
    for rec in __DUMMY_RECORDS__:
        if query in rec:
            if size == 0:
                # partitioning elements to show in one page
                return data[line * page:]
            data.append(__TR_RECORDS__[l])
            size -= 1
        l += 1

    # partitioning elements to show in one page
    # case of full data search
    return data[line * page:]


def search(request, line=10, page=1):
    query = request.GET.get('query', '')
    line = int(line)
    page = int(page)
    return render(request, 'search.html', {'query': query, 'data': get_data(query, line, page), 'page': page})


def detail(request, eid, altid=0):
    altid = int(altid)
    # gathering information from wikipedia and get images from sources
    # from eid get keyword from csv
    data = get_data(eid, 1, 0)

    # grab keywords from data
    column = (1, 2, 3, 8, 12, 29)
    keywords = ''
    for col in column:
        if col == 2:
            keywords += str(__MONTH__[int(data[0][col])]) + ' '
        else:
            keywords += data[0][col] + ' '

    titles = wikipedia.search(keywords)
    for i in xrange(len(titles)):
        titles[i] = titles[i].encode('utf-8')

    page = wikipedia.page(titles[altid])

    # get images from google using ajax from googleapis
    search_term = titles[altid]

    img_urls = []

    search_term = search_term.replace(' ', '+')
    url = 'https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + search_term
    url_request = urllib2.Request(url, None)
    response = urllib2.urlopen(url_request)
    results = simplejson.load(response)
    content = results['responseData']
    data_info = content['results']
    for url in data_info:
        img_urls.append(url['unescapedUrl'])
    img_urls = img_urls[:3]

    content = page.content
    content = re.sub('[\=]+([A-Za-z\ ])+[\=]+', __replace, content)

    relevant = list()
    i = 0
    for topic in titles:
        tmp = list()
        tmp.append(topic)
        tmp.append('/' + str(eid) + '/' + str(i) + '/')
        if i == altid:
            i += 1
            continue
        i += 1
        relevant.append(tmp)

    return render(request, 'detail.html',
                  {'eid': eid, 'data': data[0], 'page': page, 'content': content, 'img_urls': img_urls,
                   'relevant': relevant})


def __replace(match_obj):
    match_obj = match_obj.group(0)
    match_obj = match_obj.replace('=', '').strip()
    return '<br><h4>' + match_obj + '</h4>'