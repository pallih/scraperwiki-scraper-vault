# occupy world list

import scraperwiki
import lxml.html
import json
import urllib

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=List_of_Occupy_movement_protest_locations';

print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']



# occupy world list

import scraperwiki
import lxml.html
import json
import urllib

index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=List_of_Occupy_movement_protest_locations';

print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']



