import scraperwiki
import lxml.html
import datetime
import resource
import dateutil.parser
import resource

def cpu_spent():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return getattr(usage, 'ru_utime') + getattr(usage, 'ru_stime')

def fetch_oep_deliverydates(url, datastorage):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html.decode('utf-8'))
    data = { 'scrapedurl' : id }
    for tr in root.cssselect("table.defaulttable tr"):
        if 3 == len(tr.cssselect("td")):
            data = { 'scrapedurl' : url }
            #print tr
#        vtype = tr.cssselect("th")[0].text_content().strip().replace(":", "").replace(",", "")
            agency = tr.cssselect("td")[0].text_content().strip()
            deliverydate = tr.cssselect("td")[1].text_content().strip()
            if deliverydate == "Levert":
                continue
            data['agency'] = agency
            #print "D: '" + deliverydate + "'"
            data['deliverydate'] = dateutil.parser.parse(deliverydate, dayfirst=True)
            data['scrapestamputc'] = datetime.datetime.now()
            datastorage.append(data)
    return 0

datastorage = []
#fetch_oep_deliverydates("http://www.oep.no/pub/faces/statistikk.jsp?reposId=3", datastorage)
# New url before 2012-11-09
fetch_oep_deliverydates("http://www.oep.no/pub/report.xhtml?reportId=3", datastorage)
print datastorage
scraperwiki.sqlite.save(unique_keys=['agency', 'deliverydate'], data=datastorage)

print "Starting to fetch journal delivery dates " + str(datetime.datetime.now())
import scraperwiki
import lxml.html
import datetime
import resource
import dateutil.parser
import resource

def cpu_spent():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return getattr(usage, 'ru_utime') + getattr(usage, 'ru_stime')

def fetch_oep_deliverydates(url, datastorage):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html.decode('utf-8'))
    data = { 'scrapedurl' : id }
    for tr in root.cssselect("table.defaulttable tr"):
        if 3 == len(tr.cssselect("td")):
            data = { 'scrapedurl' : url }
            #print tr
#        vtype = tr.cssselect("th")[0].text_content().strip().replace(":", "").replace(",", "")
            agency = tr.cssselect("td")[0].text_content().strip()
            deliverydate = tr.cssselect("td")[1].text_content().strip()
            if deliverydate == "Levert":
                continue
            data['agency'] = agency
            #print "D: '" + deliverydate + "'"
            data['deliverydate'] = dateutil.parser.parse(deliverydate, dayfirst=True)
            data['scrapestamputc'] = datetime.datetime.now()
            datastorage.append(data)
    return 0

datastorage = []
#fetch_oep_deliverydates("http://www.oep.no/pub/faces/statistikk.jsp?reposId=3", datastorage)
# New url before 2012-11-09
fetch_oep_deliverydates("http://www.oep.no/pub/report.xhtml?reportId=3", datastorage)
print datastorage
scraperwiki.sqlite.save(unique_keys=['agency', 'deliverydate'], data=datastorage)

print "Starting to fetch journal delivery dates " + str(datetime.datetime.now())
