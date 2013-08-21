import scraperwiki
import urllib, urllib2
import json
import csv, codecs, cStringIO
import time

# Uses the JSON DBpedia interface (JSONpedia)
# http://json.it.dbpedia.org/
# to scrape (Italian) Wikipedia pages

# CSV writer
# taken from http://docs.python.org/2/library/csv.html
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeWriter:
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
        self.writer.writerow([s.encode("utf-8") for s in row])
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

def extract_data(template):
    data=dict()
    for attr,value in template.iteritems():
        data[attr]=''
        if type(value) is list:
            for v in value:
                if type(v) is unicode:
                    data[attr]+= v
                elif type(v) is dict:
                    if v['__type'] == "reference":
                        wikilink = v['label']
                        if len(v['content']) > 0:
                            k, wikilink = v['content'].popitem()
                        url = "http://it.wikipedia.org/wiki/%s" %wikilink
                        url = urllib.quote(url.encode('utf-8'))
                        data[attr] += " <a href=%s>%s</a> " %(url,v['label'])
                    elif v['__type'] == "link":
                        data[attr] = "<a href=%s>%s</a>" %(v['url'],v['description'])
                    elif v['__type'] == "template":
                        data[attr] = v['name']
                    elif v['__type'] == "inline_tag":
                        if v['name'] != 'br':
                            print type(v), v
                            print value
                    elif v['__type'] == "open_tag":
                        if v['name'] != 'small':
                            print type(v), v
                            print value
                    elif v['__type'] == "close_tag":
                        if v['name'] != 'small':
                            print type(v), v
                            print value
                    else:
                        print type(v), v
                        print value
                else:
                    print type(v), attr
        data[attr] = data[attr].strip()
    return data

# Attributes for Template:Edificio religioso
# {{Edificio religioso
# |Nome =
# |Immagine =
# |Larghezza =
# |Didascalia =
# |SiglaStato =
# |Regione =
# |Città =
# |Religione =
# |DedicatoA =
# |Ordine =
# |Diocesi =
# |AnnoConsacr =
# |AnnoSconsacr =
# |Fondatore =
# |Architetto =
# |StileArchitett =
# |InizioCostr =
# |FineCostr =
# |Demolizione =
# |Sito =
# }}

ROWDICT = {
u'NomeVoce': '',
u'Nome': '',
u'Immagine': '',
u'Larghezza': '',
u'Didascalia': '',
u'SiglaStato': '',
u'Regione': '',
u'Città': '',
u'Religione': '',
u'DedicatoA': '',
u'Ordine': '',
u'Diocesi': '',
u'AnnoConsacr': '',
u'AnnoSconsacr': '',
u'Fondatore': '',
u'Architetto': '',
u'StileArchitett': '',
u'InizioCostr': '',
u'FineCostr': '',
u'Demolizione': '',
u'Sito': ''
}


inurl = "https://dl.dropboxusercontent.com/u/1197917/it_edificio_religioso.txt"
infile = urllib2.urlopen(inurl)
inlist = infile.readlines()

outfile=open("edifici_religiosi.csv","w")
csvwriter=UnicodeWriter(outfile)
csvwriter.writerow(ROWDICT.keys())

for v in inlist:
    v=v.strip()
    rowdict=ROWDICT.copy()
    rowdict['NomeVoce']=v
    jsonurl = 'http://json.it.dbpedia.org/annotate/resource/json/it%%3A%s?filter=__type:template&flags=-Extractors,Structure,'     %(v.strip().replace(' ','_'))
    jsonpage = urllib2.urlopen(jsonurl)
    jobj = json.load(jsonpage)
    for t in jobj['result']:
        if t['name'] == "Edificio religioso":
            row = extract_data(t['content'])
            rowdict.update(row)
            #print row
            csvwriter.writerow(row.values())
        if t['name'] == "coord":
            print '"%s" has coordinates!' %v
            print t['content']
    print "* processing: %s" %v
    print jsonurl
    print "-----"
    time.sleep(5)