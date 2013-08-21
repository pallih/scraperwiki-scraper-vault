import scraperwiki
import lxml.html

def scrapeCityList(pageUrl):
    html = scraperwiki.scrape(pageUrl)
    root = lxml.html.fromstring(html)
    links = root.cssselect('td.dt1 a')
    print len(links)
    batch = []
    for link in links[1:]: #skip the first link since it's only a link to tripadvisor and not a subpage
        record = {}
        url = 'http://www.tripadvisor.co.uk/' + link.attrib['href']
        record['url'] = url
        batch.append(record)
    scraperwiki.sqlite.save(["url"],data=batch)

scrapeCityList('http://www.tripadvisor.co.uk/pages/by_city.html')