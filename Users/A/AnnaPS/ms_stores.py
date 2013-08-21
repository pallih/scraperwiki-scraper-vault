import json
import mechanize
import re
import scraperwiki
import urllib2
import lxml.html

POSTCODE_URL = 'https://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsonlist&name=uk_postcode_districts&query=select%20postcode_district%20from%20%60uk_postcode_districts%60'
BASE_URL = 'http://www.marksandspencer.com/mn/storeLocator?searchCriteria=findByAddress&jsEnabled=true&town=&postCode='

jsonurl = urllib2.urlopen(POSTCODE_URL ).read()
postcodes = json.loads(jsonurl)['data']
postcode_districts = [p[0] for p in postcodes]

def scrape_by_postcode(postcode):
    if postcode != 'E1': 
        pass
    DISTRICT_URL = BASE_URL + postcode   
    print DISTRICT_URL 
    html = scraperwiki.scrape(DISTRICT_URL)
    root = lxml.html.fromstring(html)
    stores = root.cssselect('li.addressEntry')
    for s in stores:
         store = {}
         store['name'] = s.cssselect('span.fn')[0].text_content().strip()
         addr = s.cssselect('div.adr')[0].text_content().replace('\t\n','').strip()
         print store['name'], addr 
         store['address'] = ' '.join(addr.split())
         tel = s.cssselect('div.tel')
         if len(tel) > 0:
             store['tel'] = tel[0].text_content()
         else:
             store['tel'] = None
         store['products'] = [i.strip() for i in s.cssselect('div.products span')[0].text_content().split(',')]
         store['services'] = [i.strip() for i in s.cssselect('div.services span')[0].text_content().split(',')]
         raw_hours = [h.text_content().strip() for h in s.cssselect('span.hours')]
         days = ['Wed','Thu','Fri','Sat','Sun','Mon','Tue']
         opening = {}
         if len(raw_hours) > 0:
             for i, day in enumerate(days):
                 daily_hours = [i.strip() for i in raw_hours[i].split('-')]
                 if len(daily_hours) == 2:
                     opening[day + '_opening'] = daily_hours[0]
                     opening[day + '_closing'] = daily_hours[1]
                 else: 
                     opening[day + '_opening'] = daily_hours[0]
                     opening[day + '_closing'] = daily_hours[0]
         else: 
             opening = None
         store['opening'] = opening
         print store
         scraperwiki.sqlite.save(unique_keys=["name"], data=store)
    

for p in postcode_districts:
    #print '---------------------------%s---------------------------------' % p
    #scrape_by_postcode(p)
    pass

# You can't get Irish stores out of this tool - scrape the Facebook app instead.
IRELAND_FB = 'https://pro.racedates.ie/gravitatedm/m-and-s/locations/'
html = scraperwiki.scrape(IRELAND_FB)
root = lxml.html.fromstring(html)
locations = root.cssselect('option')
for l in locations:
    #continue
    value = l.get('value')
    name = l.text_content()
    if value != 'home':
        store_url = IRELAND_FB + '/?page=' + value
        store_html = scraperwiki.scrape(store_url)
        root = lxml.html.fromstring(store_html)
        store = {}
        store['products'] = store['services'] = None
        store['name'] = name
        store['address'] = root.cssselect('div.col1 h2')[0].text_content()
        store['tel'] = root.cssselect('div.col1 h4')[0].text_content().replace('Tel: ','')
        raw_hours =  root.cssselect('tr')
        days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        opening = {}
        for i, day in enumerate(days):
            daily_hours = raw_hours[i].cssselect('td')[1].text_content().split('-')
            opening[day + '_opening'] = daily_hours[0]
            opening[day + '_closing'] = daily_hours[1]
        store['opening'] = opening
        m = re.compile(r'new google.maps.LatLng(.*?);').search(store_html)
        store['location'] = m.group(1).replace('(','').replace(')','')
        print store
        scraperwiki.sqlite.save(unique_keys=["name"], data=store)

# And finally - international stores. 
INTERNATIONAL_URL = 'http://corporate.marksandspencer.com/aboutus/where/international_stores'
browser = mechanize.Browser()
browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
browser.open(INTERNATIONAL_URL)
#print browser.response().read()
html = browser.response().get_data().replace('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">','').replace('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">','<html>')
response = mechanize.make_response(
    html, [("Content-Type", "text/html")],
INTERNATIONAL_URL, 200, "OK")
browser.set_response(response)
#browser.select_form(nr=0)