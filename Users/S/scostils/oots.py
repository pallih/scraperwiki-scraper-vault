import scraperwiki
import feedparser
import lxml.html
from datetime import tzinfo, timedelta, datetime

# Blank Python
d = feedparser.parse('http://www.giantitp.com/comics/oots.rss')
i = 0;
for num in range(0,11):
    entry = d.entries[num]
    
    try:
        result = scraperwiki.sqlite.select('* from oots where title="' + entry.title + '"')
        if len(result) > 0:
            print len(result)
            print entry.title
            continue
    except scraperwiki.sqlite.SqliteError:
        print 'Oops'

    html = scraperwiki.scrape(entry.link)
    root = lxml.html.fromstring(html)
    img = root.cssselect("td[height='*'] table td[align='center'] img:not(img[alt])")
    imglink = '<img src="http://www.giantitp.com' + img[0].get('src') + '">'
    data = {
        'title' : entry.title,
        'link' : "http://www.giantitp.com" + img[0].get('src'),
        'description' :  imglink,
        'updated' : datetime.now()
    }
    scraperwiki.sqlite.save(unique_keys=['title'], data=data, table_name="oots")

