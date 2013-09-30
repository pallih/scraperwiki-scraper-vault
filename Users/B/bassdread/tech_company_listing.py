import scraperwiki
import lxml.html 

url = 'http://www.crunchbase.com/companies'
html = scraperwiki.scrape(url)


root = lxml.html.fromstring(html)

table = root.find_class('col2_table_listing')[0]

for li in table.xpath('tr/td/ul')[0]:
    print li.xpath('a')[0].text,
    li.make_links_absolute('http://www.crunchbase.com')
    for i in li.iterlinks():
        print i[2]
    import scraperwiki
import lxml.html 

url = 'http://www.crunchbase.com/companies'
html = scraperwiki.scrape(url)


root = lxml.html.fromstring(html)

table = root.find_class('col2_table_listing')[0]

for li in table.xpath('tr/td/ul')[0]:
    print li.xpath('a')[0].text,
    li.make_links_absolute('http://www.crunchbase.com')
    for i in li.iterlinks():
        print i[2]
    