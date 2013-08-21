import scraperwiki
from scrapemark import scrape
import scraperwiki
data = scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=ci-ccurl&query=select+*+from+`swdata`&apikey=")

# Laptops data = scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=testi&query=select+*+from+`swdata`&apikey=")
line = 0
import csv
reader = csv.reader(data.splitlines())
headerline = reader.next()
for row in reader:
 line = line + 1 

 html = scraperwiki.scrape(row[0])

 scrape_data = scrape("""
{*


<tr><td width="30%"><span><a href="{{ [mobile].[url] }}">{{ [mobile].[property] }}</a>
           *}
""", html=html);

 data = [{'url':p['url'][0], 'property':p['property'][0]} for p in scrape_data['mobile']]

 scraperwiki.sqlite.save(unique_keys=["url"], data=data)


