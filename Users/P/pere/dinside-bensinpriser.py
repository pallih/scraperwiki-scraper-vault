# -*- coding: UTF-8 -*-
import scraperwiki
import lxml.html
import datetime 
import dateutil.parser
import string

scrapedurl = "http://www.dinside.no/php/oko/bensin/vis_prisliste.php"
diselurl = "http://www.dinside.no/php/oko/bensin/vis_prisliste.php?pristype=2"

def parse_date(when):
    now = datetime.datetime.now()
    nowday = now.weekday()
    daymap = {
        u'ma' : 0,
        u'ti' : 1,
        u'on' : 2,
        u'to' : 3,
        u'fr' : 4,
        u'lø' : 5,
        u'sø' : 6,
    }
    day, clock = when.split(" ")
    dayval = daymap[day]
    daydelta = (nowday - dayval) % 7
#    print nowday, " ", dayval, " ", daydelta
    delta = datetime.timedelta(days = daydelta)
    when = dateutil.parser.parse(str((now - delta).date()) + " " + str(clock))
    
#    print when
    return when

def scrape_page(tablename, colname, scrapedurl):
    html = scraperwiki.scrape(scrapedurl)
    root = lxml.html.fromstring(html)
    tabletitle = root.cssselect("td.table-title")
    header = None
    scrapestamputc = datetime.datetime.now()
    for tr in tabletitle[0].cssselect("tr"):
        if header is None:
            header = tr
            continue
        stationtype = tr[0].text_content()
        municipality = tr[1].text_content()
        stationplace = tr[2].text_content()
        stationaddress = tr[3].text_content()
        price = float(tr[4].text_content().replace(",", "."))
        when = parse_date(tr[5].text_content())
#    print tr[5].text_content()
        data = {
            colname : price,
            'label' : stationtype,
            'municipality' : string.capwords(municipality),
            'place' : stationplace,
            'address' : stationaddress,
            'when' : when,
            'scrapestamputc' : scrapestamputc,
            'scrapedurl' : scrapedurl,
        }
        print data
        scraperwiki.sqlite.save(unique_keys=['when', 'address', 'municipality'], data=data, table_name=tablename)

scrape_page("swdata", "gas95price", scrapedurl)
scrape_page("swdatadisel", "diselprice", diselurl)
