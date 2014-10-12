from csv import reader
from sas.settings import BASE_DIR


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


def init_data():
    return


def get_data(query, line, page):
    # convert query to lowercase to search by non-case sensitive
    query = unicode(query).lower()
    keywords = query.split(' ')

    print keywords

    data = list()
    size = line * page
    page -= 1
    l = 0
    for rec in __DUMMY_RECORDS__:
        # if query in rec:
        # partitioning elements to show in one page
        for key in keywords:
            if key in rec:
                data.append(__TR_RECORDS__[l])
                size -= 1
                if size == 0:
                    return data[line * page:]
            l += 1

    # partitioning elements to show in one page
    # case of full length search
    return data[line * page:]