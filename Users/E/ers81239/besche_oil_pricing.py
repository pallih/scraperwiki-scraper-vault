import scraperwiki
import datetime
import lxml.html 


html = scraperwiki.scrape("http://besche.com/")
          
root = lxml.html.fromstring(html)

para = root.cssselect("div[id='right-column'] div p b")

data = {'date':datetime.datetime.today(), 'site':'http://besche.com', 'product':'heating oil', 'price':para[0].text_content().strip('$')}

scraperwiki.sqlite.save(unique_keys=['date', 'site'], data=data)import scraperwiki
import datetime
import lxml.html 


html = scraperwiki.scrape("http://besche.com/")
          
root = lxml.html.fromstring(html)

para = root.cssselect("div[id='right-column'] div p b")

data = {'date':datetime.datetime.today(), 'site':'http://besche.com', 'product':'heating oil', 'price':para[0].text_content().strip('$')}

scraperwiki.sqlite.save(unique_keys=['date', 'site'], data=data)