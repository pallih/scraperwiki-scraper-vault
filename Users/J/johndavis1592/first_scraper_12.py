import scraperwiki

html = scraperwiki.scrape('http://www.oddschecker.com/football/english/championship/barnsley-v-cardiff-city/over-under-0.5')
#print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags

names = [el.text for el in root.xpath('//td[contains(@id,"name")]')]
#print names

bet365 = [el.text for el in root.xpath('//td[contains(@id,"B3")]')]
skybet = [el.text for el in root.xpath('//td[contains(@id,"SK")]')]
print skybet
totesport = [el.text for el in root.xpath('//td[contains(@id,"BX")]')]
betfred = [el.text for el in root.xpath('//td[contains(@id,"FR")]')]

for i in range(0, len(names)):
    data = {}
    data['bet365'] = bet365[i]
    data['skybet'] = skybet[i]
    data['betfred'] = betfred[i]
    data['winner'] = names[i]

    scraperwiki.sqlite.save(unique_keys = ['winner'], data = data) 
