import scraperwiki
import lxml.html

def parse_row(row):
    isp = dict()
    tds = row.cssselect('td')
    isp['provider'] = tds[0].text_content()
    isp['location'] = tds[1].text_content()
    isp['category'] = tds[2].text_content()
    isp['website'] = tds[3].text_content()
    isp['contact'] = tds[4].text_content()    
    global counter
    isp['id'] = counter
    print scraperwiki.sqlite.save(unique_keys=['id'], data=isp)
    counter += 1


def scrape_content(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)

    for el in root.cssselect('table.member-listing tr.On-Grey ~ tr'):
        parse_row(el)        

counter = 1

for i in range(1, 6):
    scrape_content('http://www.ispa.org.uk/about-us/our-members/?pageno=%d' % i)