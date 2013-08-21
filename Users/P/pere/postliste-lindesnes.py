# -*- coding: UTF-8 -*-
import scraperwiki
import lxml.html
import datetime
import dateutil.parser
import urllib2

# http://innsyn.lindesnes.kommune.no/Publikum/Modules/innsyn.aspx?mode=pl&SelPanel=0&ObjectType=ePhorteRegistryEntry&VariantType=Innsyn&ViewType=Table&Query=RecordDate%3a%28-14%29+AND+ResponsibleUnitID%3a%2811%29+AND+DocumentType%3a%28I%2cU%29

def fetch_url(url):
    html = None
    for n in [1, 2, 3]:
        try:
            html = scraperwiki.scrape(url)
            break
        except urllib2.URLError, e:
            print "URLError fetching " + url + ", trying again"
    return html

def make_url(id):
    url = "http://innsyn.lindesnes.kommune.no/Publikum/Modules/innsyn.aspx?mode=pl&SelPanel=0&ObjectType=ePhorteRegistryEntry&VariantType=Innsyn&ViewType=Detail&Query=ID:" + str(id)
    return url

def fetch_postjournal(agency, id, url, datastore):
#    print "Scraping " + url
    scrapestamputc = datetime.datetime.now()
    html = fetch_url(url)
    root = lxml.html.fromstring(html.decode('utf-8'))
    entry = {
        'agency' : agency,
        'scrapestamputc' : scrapestamputc,
        'scrapedurl' : url,
        'queryid' : id
    }

    for span in root.cssselect("div.robots-content span.Element"):
#        print span.text_content()
        field = None
        value = None
        if span.cssselect("h3"):
            field = span.cssselect("h3")[0].text_content().strip()
            value = span.cssselect("span.Content span")[0].text_content().strip()
        elif span.cssselect("h2"):
            field = span.cssselect("h2")[0].text_content().strip()
# FIXME
            value = ""
        elif span.cssselect("h1"):
            field = "docdesc"
            value = span.cssselect("h1")[0].text_content().strip()
#        else:
#            raise ValueError("Unexpected span")
#        print field + " = " + value
        doctypemap = {
          u'Inngående brev' : 'I',
          u'Utgående brev'  : 'U',
          u'Internt notat'  : 'N',
          u'Internt notat uten oppfølging' : 'X',
          u'Saksframlegg/innstilling' : 'S',
          u'Dokumentpost i saksmappe'  : 'Y', # Code not in NOARK, value based on http://img6.custompublish.com/getfile.php/1168825.136.pqftpqctyt/Ephorte-brukerveiledning_2.1.15.pdf?return=www.kafjord.kommune.no
        }
        if 'Type' == field:
            field = 'doctype'
            value = doctypemap[value]
        elif 'Journaldato' == field:
            field = 'recorddate'
            value =  dateutil.parser.parse(value, dayfirst=True)
        elif 'Dokumentdato' == field:
            field = 'docdate'
            value =  dateutil.parser.parse(value, dayfirst=True)
        elif u'Tilhører sak' == field:
            field = 'casedesc'
        elif 'Avsender/Mottaker' == field:
            if 'doctype' in entry and entry['doctype'] in ['U', 'X', 'N']:
                field = 'recipient'
            else:
                field = 'sender'
            td = span.cssselect("table td")
            if td:
                name = td[0].text_content().strip()
                addr = td[1].text_content().strip()
                zip  = td[2].text_content().strip()
               # print "N: '",name, "' '", addr, "' '", zip, "'"
                entry[field] = name
                entry[field + 'addr'] = addr
                entry[field + 'zip'] = zip
                field = ''

#        elif 'Saksbehandlende enhet' == field:
#        elif 'Saksbehandler' == field:
        if field is not None and '' != field:
            entry[field] = value

    print entry
    if 'doctype' in entry:
        datastore.append(entry)

agency = 'Lindesnes kommune'

def scrape_range(start, end, step, agency):
    datastore = []
    for id in range(start, end, step):
        fetch_postjournal(agency, id, make_url(id), datastore)
        if 0 < len(datastore) and 0 == (len(datastore) % 10):
            #print datastore
            scraperwiki.sqlite.save(unique_keys=['queryid'], data=datastore)
            datastore = []
    if 0 < len(datastore):
        scraperwiki.sqlite.save(unique_keys=['queryid'], data=datastore)

def scraper():
    try:
        min = scraperwiki.sqlite.select("min(queryid) as min from swdata")[0]["min"]
        max = scraperwiki.sqlite.select("min(queryid) as max from swdata")[0]["max"]
    except:
        # Random number around 2012-05-15 (ie recent when I wrote this scraper)
        min = 71836

    scrape_range(max,   max + 200,  1, agency)
    scrape_range(min-1, min - 3000, -1, agency)

if __name__ == "scraper":
    scraper()
else:
    print "Not called as scraper"