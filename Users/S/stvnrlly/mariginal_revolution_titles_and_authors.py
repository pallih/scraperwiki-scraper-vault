import scraperwiki
import lxml.html

scraperwiki.sqlite.execute('create table if not exists `swdata` (`Title` text, `Author` text)')

i = 0
while i < 100:
    url = 'http://www.marginalrevolution.com/page/' + str(i)
    html = scraperwiki.scrape(url)           
    root = lxml.html.fromstring(html)
    headlines = root.cssselect('div div.headline_area')
    post = {}
    for h in headlines:
        h2 = h.cssselect('h2')
        post['Title'] = h2[0].text_content()
        a = h.cssselect('a')
        post['Author'] = a[1].text_content()
        scraperwiki.sqlite.save(['Title'], post)
    i += 1import scraperwiki
import lxml.html

scraperwiki.sqlite.execute('create table if not exists `swdata` (`Title` text, `Author` text)')

i = 0
while i < 100:
    url = 'http://www.marginalrevolution.com/page/' + str(i)
    html = scraperwiki.scrape(url)           
    root = lxml.html.fromstring(html)
    headlines = root.cssselect('div div.headline_area')
    post = {}
    for h in headlines:
        h2 = h.cssselect('h2')
        post['Title'] = h2[0].text_content()
        a = h.cssselect('a')
        post['Author'] = a[1].text_content()
        scraperwiki.sqlite.save(['Title'], post)
    i += 1