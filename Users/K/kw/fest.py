import scraperwiki
import lxml.html
import json
import urllib
from collections import defaultdict
from pprint import pprint

def save_stats(data_dict, tbl_name="stats"):
    id = 0
    data = []
    for key in data_dict:
        id += 1
        data.append({"id":id, "region":key, "stats":data_dict[key]})
    scraperwiki.sqlite.save(unique_keys=["id"], data=data, table_name=tbl_name, verbose=2)                 


index = 'http://en.wikipedia.org/w/api.php?action=parse&format=json&page=List_of_music_festivals';
print 'Scraping ' + index + '...'
raw_json = scraperwiki.scrape(index)
#print raw_json
python_json = json.loads(raw_json)
html = python_json['parse']['text']['*']

print 'Extracting HTML...'
#print html

root = lxml.html.fromstring(html)

festival_count = 0;
country_hist = defaultdict(int)
region_hist = defaultdict(int)

print 'Processing festival list...'
data = []
for h in root:
    if h.tag == 'h3':
        # h3 span[2] - region
        region = h.cssselect('h3 span')[1].text
    if h.tag == 'h4':
        # h4 span[2] - country
        country = h.cssselect('h4 span')[1].text 
        fest_list = h.getnext()
        for fest in fest_list.cssselect('ul li'):
            # ul li a[1] - festival name
            fest_name = fest.cssselect('a')
            if fest_name:
                fest_name = fest_name[0].text
            else:
                fest_name, fest_location, fest_details = fest.text.partition(',')
            
            #basic stats
            festival_count +=1;
            country_hist[country] += 1
            region_hist[region] += 1

            #print u"{0}, {1}, {2}".format(region, country, fest_name)
            row = {"id":festival_count, "region":region, "country":country, "name":fest_name}
            data.append(row)
        pass
scraperwiki.sqlite.save(unique_keys=["id"], data=data)

pprint(json.dumps(region_hist, indent=4))
save_stats(country_hist, "country_hist")
save_stats(region_hist, "region_hist")
