from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

import mmap
import time


def read_data(filename):
    lst = list()
    with open(filename, "r+b") as f:
        # memory-mapInput the file, size 0 means whole file
        map_input = mmap.mmap(f.fileno(), 0)
        # read content via standard file methods
        for s in iter(map_input.readline, ""):
            lst.append(s)
        map_input.close()
    f.close()
    return lst

start = time.time()
# list of terrorist records
tr_records = read_data("/Users/SmAaMyA/Documents/PyCharm/Django/Terrorist_Database/globalterrorismdb_0814dist.csv")
end = time.time()
print "Time for completion", end-start
print "List length: ", len(tr_records)
print "Sample element: ", tr_records[1]

import os
import multiprocessing as mp
#
# # process file function
# def processfile(file_name, start=0, stop=0):
#     results = []
#     # if start == 0 and stop == 0:
#     #     results.append('')
#     # else:
#     with open(file_name, 'r') as fh:
#         fh.seek(start)
#         lines = fh.readlines(stop - start)
#         results.append(lines)
#
#     return results
#
# get file size and set chuck size
# file_name = '/Users/SmAaMyA/Documents/PyCharm/Django/Terrorist_Database/globalterrorismdb_0814dist.csv'
# file_size = os.path.getsize(file_name)
# split_size = 100*1024*1024
#
# # determine if it needs to be split
# if file_size > split_size:
#
#     # create pool, initialize chunk start location (cursor)
#     pool = mp.Pool(2)
#     cursor = 0
#     results = []
#     with open(file_name, 'r') as fh:
#
#          # for every chunk in the file...
#          for chunk in xrange(file_size // split_size):
#
#              # determine where the chunk ends, is it the last one?
#              if cursor + split_size > file_size:
#                  end = file_size
#              else:
#                  end = cursor + split_size
#
#              # seek to end of chunk and read next line to ensure you
#              # pass entire lines to the processfile function
#              fh.seek(end)
#              fh.readline()
#
#              # get current file location
#              end = fh.tell()
#
#              # add chunk to process pool, save reference to get results
#              proc = pool.apply_async(processfile, args=[file_name, cursor, end])
#              results.append(proc)
#
#              # setup next chunk
#              cursor = end
#
#     # close and wait for pool to finish
#     pool.close()
#     pool.join()
#
#     # iterate through results
#     for proc in results:
#         processfile_result = proc.get()
#         print processfile_result
#
# else:
#     ...process normally...