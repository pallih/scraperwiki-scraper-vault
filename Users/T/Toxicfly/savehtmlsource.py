import scraperwiki 
from scrapemark import scrape
import csv

data = scraperwiki.scrape("https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=csv&name=testi&query=select+*+from+`swdata`&apikey=")
line = 0
reader = csv.reader(data.splitlines())
headerline = reader.next()

for row in reader:
 line = line + 1 

html = scraperwiki.scrape(row[0])

scrape_data = scrape("""
{*
<div class="full_spec">
{{ [mobile].[url] }}
</div>
           *}
""", html=html);


data = [{'url':p['url'][0]} for p in scrape_data['mobile']]

scraperwiki.sqlite.save(unique_keys=["a"], data={"a":line, "bbb":data})







