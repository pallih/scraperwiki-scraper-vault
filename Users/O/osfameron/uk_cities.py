import scraperwiki
import urllib
import lxml.html
import json
import re

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=List_of_cities_in_the_United_Kingdom';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

root = lxml.html.fromstring(html)
table = root.cssselect("table.wikitable")[0]
for tr in table.cssselect('tr'):
    row = tr.cssselect('td')
    if len(row) >= 5:
        city = row[0].cssselect('a')[0].text_content()
        pop  = row[5].text_content().translate(None, ',')
        data = {"City":city, "Population":pop}
        print data
        scraperwiki.sqlite.save(["City"], data)
import scraperwiki
import urllib
import lxml.html
import json
import re

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=List_of_cities_in_the_United_Kingdom';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

root = lxml.html.fromstring(html)
table = root.cssselect("table.wikitable")[0]
for tr in table.cssselect('tr'):
    row = tr.cssselect('td')
    if len(row) >= 5:
        city = row[0].cssselect('a')[0].text_content()
        pop  = row[5].text_content().translate(None, ',')
        data = {"City":city, "Population":pop}
        print data
        scraperwiki.sqlite.save(["City"], data)
