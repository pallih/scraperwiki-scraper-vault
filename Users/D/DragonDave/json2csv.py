import scraperwiki
import cStringIO
import codecs
import cgi
import os
import csv
import sys
import json
import collections
import copy
import requests

def getpaths(fragment,sofar=[]):
    """returns a list of lists; (1, a) means x[1]['a'] is a good target"""
    if type(fragment) not in [dict, list, collections.OrderedDict]:
        return
    try:
        keys=fragment.keys()
    except AttributeError: # not a dic
        keys=range(len(fragment))
    for key in keys:
        s=list(sofar)
        s.extend([key])
        if type(fragment[key]) in [dict, list, collections.OrderedDict]:
            for i in getpaths(fragment[key], s):
                yield i
        else:
            yield s

def pullout(item,commands):
    """recursively gets items in getpaths format"""
    if commands:
        try:
            chunk = item[commands[0]]
        except IndexError:
            return ''
        except KeyError:
            return ''
        newcomm = commands[1:]
        return pullout(chunk, newcomm) or ''
    else:
        return item or ''

class UnicodeCSVWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def jsoncsv(data,nicenames=[],colnames=[],filename='unnamed',encoding=None):
    scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment;filename=%s.csv" % filename)
    writer = UnicodeCSVWriter(sys.stdout)
    if encoding:
        rawpages = (x.decode(encoding) for x in data) 
    else:
        rawpages = (x for x in data)
    pages=[json.loads(rawpage['data'], object_pairs_hook=collections.OrderedDict) for rawpage in rawpages]
        
    rawpages=None
    
    #for i in getpaths(pages[0]):
    #    print i, pullout(pages[0], i)

    # build list of potential columns
    biglist=[]
    for page in pages:
        for path in getpaths(page):
            if path not in biglist:
                biglist.append(path)
    if colnames==[]:
        colnames=sorted(list(set([x[0] for x in biglist])))
    if nicenames==[]:
        nicenames=colnames
    #print colnames
    # prune and sort
    newbiglist=[]
    for col in colnames:
        for i in biglist:
            if i[0]==col:
                newbiglist.append(i)

    # nice columnname 
    nicelist=copy.deepcopy(newbiglist)
    for item in nicelist:
        item[0]=nicenames[colnames.index(item[0])]
    names=[]
    for i in nicelist:
        names.append(u'_'.join([unicode(j) for j in i]))
    
    writer.writerow(names)
    
    # output rows
    for page in pages:
        rowdata=[pullout(page, i) for i in newbiglist]
        writer.writerow(rowdata)

if __name__=='scraper':
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    paramlist=['url','nicenames','colnames','encoding','filename','data']
    jqs={}
    for item in paramlist:
        try:
            jqs[item]=json.loads(qs[item])
        except KeyError:
            jqs[item]=None
    if jqs['url'] and jqs['data']==None:
        inputfile=requests.get(jqs['url'], verify=False).content
        jqs['data']=json.loads(inputfile)
    for i in paramlist:
        if jqs[i]==None or i=='url':
            del jqs[i]
    jsoncsv(**jqs)
import scraperwiki
import cStringIO
import codecs
import cgi
import os
import csv
import sys
import json
import collections
import copy
import requests

def getpaths(fragment,sofar=[]):
    """returns a list of lists; (1, a) means x[1]['a'] is a good target"""
    if type(fragment) not in [dict, list, collections.OrderedDict]:
        return
    try:
        keys=fragment.keys()
    except AttributeError: # not a dic
        keys=range(len(fragment))
    for key in keys:
        s=list(sofar)
        s.extend([key])
        if type(fragment[key]) in [dict, list, collections.OrderedDict]:
            for i in getpaths(fragment[key], s):
                yield i
        else:
            yield s

def pullout(item,commands):
    """recursively gets items in getpaths format"""
    if commands:
        try:
            chunk = item[commands[0]]
        except IndexError:
            return ''
        except KeyError:
            return ''
        newcomm = commands[1:]
        return pullout(chunk, newcomm) or ''
    else:
        return item or ''

class UnicodeCSVWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def jsoncsv(data,nicenames=[],colnames=[],filename='unnamed',encoding=None):
    scraperwiki.utils.httpresponseheader("Content-Type", "text/csv")
    scraperwiki.utils.httpresponseheader("Content-Disposition", "attachment;filename=%s.csv" % filename)
    writer = UnicodeCSVWriter(sys.stdout)
    if encoding:
        rawpages = (x.decode(encoding) for x in data) 
    else:
        rawpages = (x for x in data)
    pages=[json.loads(rawpage['data'], object_pairs_hook=collections.OrderedDict) for rawpage in rawpages]
        
    rawpages=None
    
    #for i in getpaths(pages[0]):
    #    print i, pullout(pages[0], i)

    # build list of potential columns
    biglist=[]
    for page in pages:
        for path in getpaths(page):
            if path not in biglist:
                biglist.append(path)
    if colnames==[]:
        colnames=sorted(list(set([x[0] for x in biglist])))
    if nicenames==[]:
        nicenames=colnames
    #print colnames
    # prune and sort
    newbiglist=[]
    for col in colnames:
        for i in biglist:
            if i[0]==col:
                newbiglist.append(i)

    # nice columnname 
    nicelist=copy.deepcopy(newbiglist)
    for item in nicelist:
        item[0]=nicenames[colnames.index(item[0])]
    names=[]
    for i in nicelist:
        names.append(u'_'.join([unicode(j) for j in i]))
    
    writer.writerow(names)
    
    # output rows
    for page in pages:
        rowdata=[pullout(page, i) for i in newbiglist]
        writer.writerow(rowdata)

if __name__=='scraper':
    qs = dict(cgi.parse_qsl(os.getenv("QUERY_STRING")))
    paramlist=['url','nicenames','colnames','encoding','filename','data']
    jqs={}
    for item in paramlist:
        try:
            jqs[item]=json.loads(qs[item])
        except KeyError:
            jqs[item]=None
    if jqs['url'] and jqs['data']==None:
        inputfile=requests.get(jqs['url'], verify=False).content
        jqs['data']=json.loads(inputfile)
    for i in paramlist:
        if jqs[i]==None or i=='url':
            del jqs[i]
    jsoncsv(**jqs)
