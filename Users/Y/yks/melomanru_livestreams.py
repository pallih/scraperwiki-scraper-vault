import scraperwiki
import dateutil.parser
import datetime

html = scraperwiki.scrape("http://www.meloman.ru/?id=33")
#print html


import lxml.html
root = lxml.html.fromstring(html)
for el in root.cssselect("div.content li a"):
    ev_title = el.text_content()
#    print ev_title
    if ev_title[6:8]=="20":
        ev_date = dateutil.parser.parse(ev_title[:10], dayfirst=True).date()
        if ev_date >= datetime.date.today():
            ev_html = scraperwiki.scrape(el.attrib['href'])
            ev_root = lxml.html.fromstring(ev_html)
            pl = ev_root.cssselect("div.place a")[0].text_content()
            tm = ev_root.cssselect("div.time")[0].text_content()
            img = ev_root.cssselect("div#content-right img")
            title2 = ev_root.cssselect("div.content h1")[0].text_content()
            ev_text = ev_root.cssselect("div#content-left")[0].text_content()
            data = {
                'title' : ev_title[12:-15],
                'title2' : title2,
                'date' : ev_date,
                'time' : tm[-5:],
                'link' : el.attrib['href'],
                'image' : "http://www.meloman.ru/" + img[0].attrib['src'],
                'text' : ev_text,
                'place' : pl,
                'source' : "www.meloman.ru"
            }
            scraperwiki.sqlite.save(['title','date','time','source'],data,'liveevents')
#            print data['date'],data['time'],data['title'], data['place'], data['image']
#    print el.text_content()import scraperwiki
import dateutil.parser
import datetime

html = scraperwiki.scrape("http://www.meloman.ru/?id=33")
#print html


import lxml.html
root = lxml.html.fromstring(html)
for el in root.cssselect("div.content li a"):
    ev_title = el.text_content()
#    print ev_title
    if ev_title[6:8]=="20":
        ev_date = dateutil.parser.parse(ev_title[:10], dayfirst=True).date()
        if ev_date >= datetime.date.today():
            ev_html = scraperwiki.scrape(el.attrib['href'])
            ev_root = lxml.html.fromstring(ev_html)
            pl = ev_root.cssselect("div.place a")[0].text_content()
            tm = ev_root.cssselect("div.time")[0].text_content()
            img = ev_root.cssselect("div#content-right img")
            title2 = ev_root.cssselect("div.content h1")[0].text_content()
            ev_text = ev_root.cssselect("div#content-left")[0].text_content()
            data = {
                'title' : ev_title[12:-15],
                'title2' : title2,
                'date' : ev_date,
                'time' : tm[-5:],
                'link' : el.attrib['href'],
                'image' : "http://www.meloman.ru/" + img[0].attrib['src'],
                'text' : ev_text,
                'place' : pl,
                'source' : "www.meloman.ru"
            }
            scraperwiki.sqlite.save(['title','date','time','source'],data,'liveevents')
#            print data['date'],data['time'],data['title'], data['place'], data['image']
#    print el.text_content()