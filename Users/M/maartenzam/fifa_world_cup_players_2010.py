import scraperwiki
import urllib
import lxml.html
import json
import re

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=2010_FIFA_World_Cup_squads';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

root = lxml.html.fromstring(html)

for x in xrange(0,32):
    table = root.cssselect("table.sortable")[x]
    for tr in table.cssselect('tr'):
        row = tr.cssselect('td')
        if len(row) >= 5:
            number = row[0].text_content()
            position = row[1].text_content()
            name = row[2].text_content()
            dob = row[3].text_content()
            caps = row[4].text_content()
            club  = row[5].text_content()
            data = {"Number":number, "Position":position, "Name":name, "Date of birth":dob, "Caps":caps, "Club":club}
            print data
            scraperwiki.sqlite.save(["Name"], data)
import scraperwiki
import urllib
import lxml.html
import json
import re

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=2010_FIFA_World_Cup_squads';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

root = lxml.html.fromstring(html)

for x in xrange(0,32):
    table = root.cssselect("table.sortable")[x]
    for tr in table.cssselect('tr'):
        row = tr.cssselect('td')
        if len(row) >= 5:
            number = row[0].text_content()
            position = row[1].text_content()
            name = row[2].text_content()
            dob = row[3].text_content()
            caps = row[4].text_content()
            club  = row[5].text_content()
            data = {"Number":number, "Position":position, "Name":name, "Date of birth":dob, "Caps":caps, "Club":club}
            print data
            scraperwiki.sqlite.save(["Name"], data)
import scraperwiki
import urllib
import lxml.html
import json
import re

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=2010_FIFA_World_Cup_squads';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

root = lxml.html.fromstring(html)

for x in xrange(0,32):
    table = root.cssselect("table.sortable")[x]
    for tr in table.cssselect('tr'):
        row = tr.cssselect('td')
        if len(row) >= 5:
            number = row[0].text_content()
            position = row[1].text_content()
            name = row[2].text_content()
            dob = row[3].text_content()
            caps = row[4].text_content()
            club  = row[5].text_content()
            data = {"Number":number, "Position":position, "Name":name, "Date of birth":dob, "Caps":caps, "Club":club}
            print data
            scraperwiki.sqlite.save(["Name"], data)
import scraperwiki
import urllib
import lxml.html
import json
import re

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=2010_FIFA_World_Cup_squads';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

root = lxml.html.fromstring(html)

for x in xrange(0,32):
    table = root.cssselect("table.sortable")[x]
    for tr in table.cssselect('tr'):
        row = tr.cssselect('td')
        if len(row) >= 5:
            number = row[0].text_content()
            position = row[1].text_content()
            name = row[2].text_content()
            dob = row[3].text_content()
            caps = row[4].text_content()
            club  = row[5].text_content()
            data = {"Number":number, "Position":position, "Name":name, "Date of birth":dob, "Caps":caps, "Club":club}
            print data
            scraperwiki.sqlite.save(["Name"], data)
