import scraperwiki
import lxml.html

max_page   = 34
base_url   = 'http://www.swordandlaser.com/home/category/podcast?currentPage='

for page_count in range(1, max_page+1):
    html = scraperwiki.scrape(base_url + str(page_count))
    root = lxml.html.fromstring(html)
    print str(page_count);

    for podcast in root.cssselect("p[class='enclosureWrapper'] a"):
        data = {
          'name' : podcast.text_content(),
          'url'  : podcast.attrib.get('href')
        }
        scraperwiki.sqlite.save(unique_keys=['name'], data=data);

    
