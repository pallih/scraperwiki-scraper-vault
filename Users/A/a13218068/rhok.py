import scraperwiki
import lxml.html
import dateutil.parser

html = scraperwiki.scrape("http://www.volontaireslausannois.ch/html/index.php?c=15");
root = lxml.html.fromstring(html)
content = root.cssselect("table.contenu tr td")
for el in content:
    title = el.cssselect("b i")
    date = el.cssselect("br")
    startdate = None
    enddate = None
    if( len(title) > 0):
        tmp = date[0].tail
        if( tmp.startswith("Le") ):
            tmp = tmp[2:]
            startdate = dateutil.parser.parse(tmp)
        elif ( tmp.startswith("Du") ):
            pos = tmp.find("au");
            t1 = tmp[2:pos];
            t2 = tmp[pos+3:];
            startdate = dateutil.parser.parse(t1)
            enddate = dateutil.parser.parse(t2)
        if( enddate is None):
            data = {
                'title' : title[0].text,
                'datestart' : startdate.strftime('%Y-%m-%d')
            }
        else:
            data = {
                'title' : title[0].text,
                'datestart' : startdate.strftime('%Y-%m-%d'),
                'dateend' : enddate.strftime('%Y-%m-%d')
            }
        print data
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)

import scraperwiki
import lxml.html
import dateutil.parser

html = scraperwiki.scrape("http://www.volontaireslausannois.ch/html/index.php?c=15");
root = lxml.html.fromstring(html)
content = root.cssselect("table.contenu tr td")
for el in content:
    title = el.cssselect("b i")
    date = el.cssselect("br")
    startdate = None
    enddate = None
    if( len(title) > 0):
        tmp = date[0].tail
        if( tmp.startswith("Le") ):
            tmp = tmp[2:]
            startdate = dateutil.parser.parse(tmp)
        elif ( tmp.startswith("Du") ):
            pos = tmp.find("au");
            t1 = tmp[2:pos];
            t2 = tmp[pos+3:];
            startdate = dateutil.parser.parse(t1)
            enddate = dateutil.parser.parse(t2)
        if( enddate is None):
            data = {
                'title' : title[0].text,
                'datestart' : startdate.strftime('%Y-%m-%d')
            }
        else:
            data = {
                'title' : title[0].text,
                'datestart' : startdate.strftime('%Y-%m-%d'),
                'dateend' : enddate.strftime('%Y-%m-%d')
            }
        print data
        scraperwiki.sqlite.save(unique_keys=['title'], data=data)

