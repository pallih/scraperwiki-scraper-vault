# Blank Python
import scrapemark
import scraperwiki
from urllib2 import Request, urlopen, URLError, HTTPError
import lxml.etree
import lxml.html.clean
import simplejson as json
#from lxml.html.clean import clean_html #http://codespeak.net/lxml/lxmlhtml.html#cleaning-up-html
from datetime import datetime
import csv

url = "https://spreadsheets.google.com/spreadsheet/pub?hl=fr&hl=fr&key=0AmwtCKEN_vuwdElCajhHMzdGZHAtdElhdWRRaFFQTlE&single=true&gid=0&output=csv"
scraperwiki.sqlite.save_var('data_columns', ['VILLE','CP','AGENDA','SOURCE','LAT','LNG'])
#f = urlopen(url)
req = Request(url)
try:
    f= urlopen(req)
except HTTPError, e:
    print 'impossible d effectuer la requète sur le fichier source'
    print 'Error code: ', e.code
except URLError, e:
    print 'Impossible d atteindre le serveur'
    print 'Reason: ', e.reason
else:
    lines = f.readlines()
    clist = list(csv.reader(lines))
    header = clist.pop(0)   # set 'header' to be the first row of the CSV file
    for row in clist :
        ville = dict(zip(header, row))
        if 'PATTERN' in ville.keys() :
        #if ville['NOM'] == 'MONTVENDRE' :
            req = Request(ville['SCRAP_SOURCE'])
            try:
                response = urlopen(req)
            except HTTPError, e:
                print 'impossible d effectuer la requète'
                print 'Error code: ', e.code
            except URLError, e:
                print 'Impossible d atteindre le serveur'
                print 'Reason: ', e.reason
            else:   
                #html =scraperwiki.scrape(ville['SCRAP_SOURCE'])
                #if(html) :
                agenda = scrapemark.scrape(ville['PATTERN'],url=ville['SCRAP_SOURCE'])
                print ville['NOM'],ville['PATTERN'],ville['SCRAP_SOURCE']
                #print agenda
                if len(agenda)>0:
                    print json.dumps(agenda)
                    scraperwiki.sqlite.save(unique_keys=["VILLE"], data={"VILLE":ville['NOM'].upper(), "CP":ville['CP'],"AGENDA":json.dumps(agenda),"SOURCE":ville['SOURCE'],"date":datetime.now(),"latlng":(float(ville['LAT']),float(ville['LNG']))})# Blank Python
import scrapemark
import scraperwiki
from urllib2 import Request, urlopen, URLError, HTTPError
import lxml.etree
import lxml.html.clean
import simplejson as json
#from lxml.html.clean import clean_html #http://codespeak.net/lxml/lxmlhtml.html#cleaning-up-html
from datetime import datetime
import csv

url = "https://spreadsheets.google.com/spreadsheet/pub?hl=fr&hl=fr&key=0AmwtCKEN_vuwdElCajhHMzdGZHAtdElhdWRRaFFQTlE&single=true&gid=0&output=csv"
scraperwiki.sqlite.save_var('data_columns', ['VILLE','CP','AGENDA','SOURCE','LAT','LNG'])
#f = urlopen(url)
req = Request(url)
try:
    f= urlopen(req)
except HTTPError, e:
    print 'impossible d effectuer la requète sur le fichier source'
    print 'Error code: ', e.code
except URLError, e:
    print 'Impossible d atteindre le serveur'
    print 'Reason: ', e.reason
else:
    lines = f.readlines()
    clist = list(csv.reader(lines))
    header = clist.pop(0)   # set 'header' to be the first row of the CSV file
    for row in clist :
        ville = dict(zip(header, row))
        if 'PATTERN' in ville.keys() :
        #if ville['NOM'] == 'MONTVENDRE' :
            req = Request(ville['SCRAP_SOURCE'])
            try:
                response = urlopen(req)
            except HTTPError, e:
                print 'impossible d effectuer la requète'
                print 'Error code: ', e.code
            except URLError, e:
                print 'Impossible d atteindre le serveur'
                print 'Reason: ', e.reason
            else:   
                #html =scraperwiki.scrape(ville['SCRAP_SOURCE'])
                #if(html) :
                agenda = scrapemark.scrape(ville['PATTERN'],url=ville['SCRAP_SOURCE'])
                print ville['NOM'],ville['PATTERN'],ville['SCRAP_SOURCE']
                #print agenda
                if len(agenda)>0:
                    print json.dumps(agenda)
                    scraperwiki.sqlite.save(unique_keys=["VILLE"], data={"VILLE":ville['NOM'].upper(), "CP":ville['CP'],"AGENDA":json.dumps(agenda),"SOURCE":ville['SOURCE'],"date":datetime.now(),"latlng":(float(ville['LAT']),float(ville['LNG']))})