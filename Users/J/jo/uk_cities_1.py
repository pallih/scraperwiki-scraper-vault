import scraperwiki
import urllib
import lxml.html
import json
import re

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=The_Muppet_Show';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

root = lxml.html.fromstring(html)
table = root.cssselect("table.wikitable")[0]
for tr in table.cssselect('tr')[1:-1]:
    muppet = tr[0].text_content()
    info = tr[2].text_content()
    info = re.sub("[[]"+"[0-9]"+"]", "", info)
    data = {"Muppet":muppet, "Info":info}
    print data
    scraperwiki.sqlite.save(["Muppet"], data)
import scraperwiki
import urllib
import lxml.html
import json
import re

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=The_Muppet_Show';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

root = lxml.html.fromstring(html)
table = root.cssselect("table.wikitable")[0]
for tr in table.cssselect('tr')[1:-1]:
    muppet = tr[0].text_content()
    info = tr[2].text_content()
    info = re.sub("[[]"+"[0-9]"+"]", "", info)
    data = {"Muppet":muppet, "Info":info}
    print data
    scraperwiki.sqlite.save(["Muppet"], data)
