from csv import reader
import re
import time
import urllib2

from django.shortcuts import render
import simplejson
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

    t1 = time.time()
    with open(BASE_DIR + '/media/globalterrorismdb_0814dist.csv', 'rb') as csv_file:
        row_reader = reader(csv_file, delimiter=',', quotechar='"')
        for row in row_reader:
            # case sensitive

            if query in row:
                data.append(row)

                # case insensitive

                # if query.lower() in (tmp_row.lower() for tmp_row in row):
                # data.append(row)

                # multiple words

                # if any(keyword in row for keyword in query.split()):
                # data.append(row)

                # multiple words and case insensitive

                # if any(keyword.lower() in (tmp_row.lower() for tmp_row in row) for keyword in query.split()):
                # data.append(row)
    csv_file.close()
    t2 = time.time()
    print "Time = " + str(t2 - t1)

    # sort by date, most recent event come first
    data.reverse()
    # partitioning elements to show in one page
    data = data[line * page:line * page + line]
    print(len(data[0]))

    return data


def search(request, line=10, page=1):
    query = request.GET.get('query', '')
    line = int(line)
    page = int(page)
    return render(request, 'search.html', {'query': query, 'data': getdata(query, line, page - 1), 'page': page})


def detail(request, eid, altid=0):
    altid = int(altid)
    # gathering information from wikipedia and get images from sources
    # from eid get keyword from csv
    data = getdata(eid, 1, 0)

    # grab keywords from data
    column = (1, 2, 3, 8, 12, 29)
    keywords = ''
    for col in column:
        if col == 2:
            keywords += str(MONTH[int(data[0][col])]) + ' '
        else:
            keywords += data[0][col] + ' '

    titles = wikipedia.search(keywords)
    for i in xrange(len(titles)):
        titles[i] = titles[i].encode('utf-8')

    page = wikipedia.page(titles[altid])

    # get images from google using ajax from googleapis
    searchTerm = titles[altid]

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


def __replace(matchobj):
    matchobj = matchobj.group(0)
    matchobj = matchobj.replace('=', '').strip()
    return '<br><h4>' + matchobj + '</h4>'