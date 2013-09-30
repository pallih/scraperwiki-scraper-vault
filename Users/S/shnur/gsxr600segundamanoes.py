import datetime
import lxml.html
import scraperwiki

# Scrape GSX-R600 ads from segundamano.es

URL = "http://www.segundamano.es/motos-de-segunda-mano-barcelona/gsx-r600.htm"
USER_AGENT = "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4"


html = scraperwiki.scrape(URL, user_agent=USER_AGENT)
root = lxml.html.fromstring(html)
for ul in root.cssselect("ul.list_ads_row"):
    a = ul.cssselect('li.image a')
    if not a:
        continue
    url = a[0].attrib['href']
    img = ul.cssselect('li.image img')[0].attrib['data-original']
    title = ul.cssselect('li.subject a.subjectTitle')[0].text.encode('utf-8')
    price = ul.cssselect('li.subject a.subjectPrice')[0].text.encode('utf-8')
    location = ul.cssselect('li.zone a')[0].text.encode('utf-8')

    scraperwiki.sqlite.save(['url'], dict(
        url=url,
        img=img,
        title=title,
        price=price,
        location=location
    ), table_name='motos')
import datetime
import lxml.html
import scraperwiki

# Scrape GSX-R600 ads from segundamano.es

URL = "http://www.segundamano.es/motos-de-segunda-mano-barcelona/gsx-r600.htm"
USER_AGENT = "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4"


html = scraperwiki.scrape(URL, user_agent=USER_AGENT)
root = lxml.html.fromstring(html)
for ul in root.cssselect("ul.list_ads_row"):
    a = ul.cssselect('li.image a')
    if not a:
        continue
    url = a[0].attrib['href']
    img = ul.cssselect('li.image img')[0].attrib['data-original']
    title = ul.cssselect('li.subject a.subjectTitle')[0].text.encode('utf-8')
    price = ul.cssselect('li.subject a.subjectPrice')[0].text.encode('utf-8')
    location = ul.cssselect('li.zone a')[0].text.encode('utf-8')

    scraperwiki.sqlite.save(['url'], dict(
        url=url,
        img=img,
        title=title,
        price=price,
        location=location
    ), table_name='motos')
