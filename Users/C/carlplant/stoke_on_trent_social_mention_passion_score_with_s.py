import scraperwiki
import lxml.html
import datetime
html = scraperwiki.scrape("http://www.socialmention.com/search?t=all&q=stoke+on+trent&btnG=Search")
print html
now = datetime.datetime.now()
root = lxml.html.fromstring(html)
for positive in root.cssselect("div#column_left, div#top_keywords tr")[1]:    
    print positive.text
for neutral in root.cssselect("div#column_left, div#top_keywords tr")[2]:
    print neutral.text
for negative in root.cssselect("div#column_left, div#top_keywords tr")[3]:
    print negative.text

    
scraperwiki.sqlite.save(unique_keys=[], data={'scrapedate' : now, 'positive': positive.text, 'neutral' : neutral.text, 'negative' : negative.text}, table_name='sent')
import scraperwiki
import lxml.html
import datetime
html = scraperwiki.scrape("http://www.socialmention.com/search?t=all&q=stoke+on+trent&btnG=Search")
print html
now = datetime.datetime.now()
root = lxml.html.fromstring(html)
for positive in root.cssselect("div#column_left, div#top_keywords tr")[1]:    
    print positive.text
for neutral in root.cssselect("div#column_left, div#top_keywords tr")[2]:
    print neutral.text
for negative in root.cssselect("div#column_left, div#top_keywords tr")[3]:
    print negative.text

    
scraperwiki.sqlite.save(unique_keys=[], data={'scrapedate' : now, 'positive': positive.text, 'neutral' : neutral.text, 'negative' : negative.text}, table_name='sent')
