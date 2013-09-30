import scraperwiki
import lxml.html
import re

def scrape_content(url):
    return lxml.html.fromstring(scraperwiki.scrape(url))

def get_latlang(html):
    return re.search('(?<=LatLng\().*', html).group(0).rstrip(');').split(',')

def scrape_fish(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    fish = dict()
    fish['Latitude'], fish['Langitude'] = get_latlang(html)
    fish['Langitude'] = fish['Langitude'].lstrip(' ')
    fish['Name'] = root.cssselect('div.content-list > h2')[0].text_content()
    fish['url'] = url
    data = root.cssselect('div.content-list div')    
    i = 0
    for el in data:
        if (i%2 == 1):
            fish[data[i-1].text_content().rstrip(': ').replace(' ', '_')] = data [i].text_content()
        i += 1
    global counter
    fish['id'] = counter
    print scraperwiki.sqlite.save(unique_keys=['id'], data=fish)
    counter += 1

def prefix_domain(suffix):
    return 'http://canalrivertrust.org.uk' + suffix

def scrape_search(url):
    root = scrape_content(url)
    for el in root.cssselect('ul.page-specific-search-results > li'):
        scrape_fish(prefix_domain(el.cssselect('a')[0].attrib['href']))
    #next_link = root.cssselect('li.next')[0]
    #if next_link is not None:        
    #    scrape_search(prefix_domain(next_link.cssselect('a')[0].attrib['href']))
    
counter = 1
for i in range(196,243):
    src = 'http://canalrivertrust.org.uk/see-and-do/fishing?location=&range=&submit=Search&ps_search_handler=Fishing&document_type=(Fishery\EaFishery+Fishery\CrtFishery+Maps\WaterwayWanderer)&page_num=' + str(i)
    scrape_search(src)

import scraperwiki
import lxml.html
import re

def scrape_content(url):
    return lxml.html.fromstring(scraperwiki.scrape(url))

def get_latlang(html):
    return re.search('(?<=LatLng\().*', html).group(0).rstrip(');').split(',')

def scrape_fish(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    fish = dict()
    fish['Latitude'], fish['Langitude'] = get_latlang(html)
    fish['Langitude'] = fish['Langitude'].lstrip(' ')
    fish['Name'] = root.cssselect('div.content-list > h2')[0].text_content()
    fish['url'] = url
    data = root.cssselect('div.content-list div')    
    i = 0
    for el in data:
        if (i%2 == 1):
            fish[data[i-1].text_content().rstrip(': ').replace(' ', '_')] = data [i].text_content()
        i += 1
    global counter
    fish['id'] = counter
    print scraperwiki.sqlite.save(unique_keys=['id'], data=fish)
    counter += 1

def prefix_domain(suffix):
    return 'http://canalrivertrust.org.uk' + suffix

def scrape_search(url):
    root = scrape_content(url)
    for el in root.cssselect('ul.page-specific-search-results > li'):
        scrape_fish(prefix_domain(el.cssselect('a')[0].attrib['href']))
    #next_link = root.cssselect('li.next')[0]
    #if next_link is not None:        
    #    scrape_search(prefix_domain(next_link.cssselect('a')[0].attrib['href']))
    
counter = 1
for i in range(196,243):
    src = 'http://canalrivertrust.org.uk/see-and-do/fishing?location=&range=&submit=Search&ps_search_handler=Fishing&document_type=(Fishery\EaFishery+Fishery\CrtFishery+Maps\WaterwayWanderer)&page_num=' + str(i)
    scrape_search(src)

