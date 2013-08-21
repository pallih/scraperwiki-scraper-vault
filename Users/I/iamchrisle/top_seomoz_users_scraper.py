import scraperwiki
import lxml.html
import urlparse

url = 'http://www.seomoz.org/users'

html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)



url2 = 'http://www.seomoz.org/users/index?page=2'

html = scraperwiki.scrape(url2)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)



url3 = 'http://www.seomoz.org/users/index?page=3'

html = scraperwiki.scrape(url3)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)



url4 = 'http://www.seomoz.org/users/index?page=4'

html = scraperwiki.scrape(url4)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)



url5 = 'http://www.seomoz.org/users/index?page=5'

html = scraperwiki.scrape(url5)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)



url6 = 'http://www.seomoz.org/users/index?page=6'

html = scraperwiki.scrape(url6)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)



url7 = 'http://www.seomoz.org/users/index?page=7'

html = scraperwiki.scrape(url7)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)



url8 = 'http://www.seomoz.org/users/index?page=8'

html = scraperwiki.scrape(url8)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)



url9 = 'http://www.seomoz.org/users/index?page=9'

html = scraperwiki.scrape(url9)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)



url10 = 'http://www.seomoz.org/users/index?page=10'

html = scraperwiki.scrape(url10)
root = lxml.html.fromstring(html)


for tr in root.cssselect("table tr"):
    tds = tr.cssselect("td")
    a = tr.cssselect("td a")
    img = tr.cssselect("td a img")

    if len(tds)>1:
        data = {'Rank' : int(tds[0].text_content()),'Profile' : a[1].attrib['href'],'Name' : img[0].attrib['alt'],'Mozpoints' : int(tds[2].text_content()),'Blog Posts' : int(tds[3].text_content()),'YouMoz Posts' : int(tds[4].text_content()),'Blog Comments' :int( tds[5].text_content()),'Thumbs Up' : int(tds[6].text_content()),'Thumbs Down' : int(tds[7].text_content())}
        print data
        scraperwiki.sqlite.save(unique_keys=['Rank'], data=data)
