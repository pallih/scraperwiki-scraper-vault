import scraperwiki
from lxml.html import fromstring, tostring
from lxml.cssselect import CSSSelector
from scraperwiki import datastore

historical = False
startyear = 1992
startweek = 1

def cleanint(string):
    try:
        return int(string.replace(",", ""))
    except:
        return 0

def cleanfloat(string):
    try:
        return float(string)
    except:
        return 0.0

def cleantime(string):
    try:
        hrs, mins = string.split(":", 1)
        return int(hrs) * 60 + int(mins)
    except:
        return 0

def scrapepage(url):
    html = scraperwiki.scrape(url)
    page = fromstring(html)
    print page
    datevalue = CSSSelector('select#period option[selected]')(page)[0]['value']
    print datevalue
    
    for row in CSSSelector('table.datagrid tbody tr')(page):
        columns = CSSSelector('td')(row)
        data = {'channel': columns[0].text,
            'dailyreach': cleanint(columns[1].text) * 1000,
            'dailyreach_percent': cleanfloat(columns[2].text),
            'weeklyreach': cleanint(columns[3].text) * 1000,
            'weeklyreach_percent': cleanfloat(columns[4].text),
            'weeklyviewing': cleantime(columns[5].text),
            'share': cleanfloat(columns[6].text)}
        datastore.save(unique_keys=['channel'], data=data)


if not historical:
    scrapepage('http://www.barb.co.uk/report/weeklyViewing')