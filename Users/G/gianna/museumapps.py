import scraperwiki
import lxml.html
import json
import urllib

# Blank Python
# print scraperwiki. scrape("http://en.wikipedia.org/w/api.php?action=parse&format=json&page=List_of_Occupy_movement_protest_locations_in_California")


# Blank Python
#print scraperwiki.scrape("http://www.museumsandtheweb.com/mw2012/best/nominees")

index = 'http://www.museumsandtheweb.com/mw2012/best/nominees';
# parsing: if this (below) print command works, we know that the script is correct
print 'Scraping ' + index + '...'



raw_json = scraperwiki.scrape(index)
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']



