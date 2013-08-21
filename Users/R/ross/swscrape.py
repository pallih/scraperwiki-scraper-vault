from lxml.html import fromstring
import scraperwiki
import time

# Blank Python

#.code_object_line h3
# a[0] is author, a[1] is href


def read_page(page_html):
    items = []
    page = fromstring(page_html)
    blocks = page.cssselect('.code_object_line h3')
    for h in blocks:
        links = h.cssselect('a')    
        author = links[0].text_content()
        name = links[1].get('href').split('/')[2]
        items.append( {'name': name, 'author': author} )
    scraperwiki.sqlite.save(['name'], items, table_name='scrapers')
    return len(items)

def get_names():
    for x in xrange(516, 1000):
        l = 'https://classic.scraperwiki.com/browse/?page={0}'.format(x)
        html = scraperwiki.scrape(l)    
        n = read_page(html)
        if n == 0:
            break
        time.sleep(0.5)
    
def get_data():
    scraperwiki.sqlite.attach('scrapers')
    res = scraperwiki.sqlite.select('name,author from `scrapers` where name not in (select name from `swdata`)')
    l = []
    print len(res), "items to process"
    for row in res:
        name = row['name']
        author = row['author']
        try:
            data = scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/scraper/getinfo?format=jsondict&name={0}&version=-1&quietfields=runevents%7Cdatasummary%7Cuserroles%7Chistory".format(name))
        except:
            print "Failed to fetch API for ", name
            continue

        if not data:
            print "Bailed on {0}".format(name)
            continue
        l.append({'name': name, 'author': author, 'data': data})

        if len(l) == 100:
            scraperwiki.sqlite.save(['name'], l )
            l = []
            time.sleep(1)
    if l:
        scraperwiki.sqlite.save(['name'], l )

get_data()
#get_names()
