# Companies listed on LSE from Wikipedia
import scraperwiki
import lxml.html

categories = ['http://en.wikipedia.org/wiki/Category:Companies_listed_on_the_London_Stock_Exchange',]

for category_url in categories:
    category_url_next = category_url
    while category_url_next is not None:
        tree = lxml.html.parse(category_url_next)
        
        for a in tree.xpath('//td/ul/li/a'):
            scraperwiki.sqlite.save(['url'], {'name': a.text, 'category_url': category_url, 'url': "http://en.wikipedia.org%s" % a.attrib['href']}, table_name='companies')
    
        next_a = tree.xpath('//div[@id="mw-pages"]/a[.="next 200"]')
        if next_a:
            print "Continuing on %s" % category_url
            category_url_next = "http://en.wikipedia.org%s" % next_a[0].attrib['href']
        else:
            category_url_next = None
