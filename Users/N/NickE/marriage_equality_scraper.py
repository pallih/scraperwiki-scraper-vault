###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.australianmarriageequality.com/whereyourmpstands/states/NSW/')


import lxml.html
root = lxml.html.fromstring(html) 
federalmember = root.cssselect('div.federal-member') 
for div in federalmember:
    data = {}
    data['member'] = div.cssselect("div.federal-member-name")[0].text
    data['description'] = div.cssselect("div.federal-member-description")[0].text
    data['position'] = div.cssselect("div.federal-member-position")[0].text
    print data
    scraperwiki.sqlite.save(unique_keys=["member"], data=data)
        ###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.australianmarriageequality.com/whereyourmpstands/states/NSW/')


import lxml.html
root = lxml.html.fromstring(html) 
federalmember = root.cssselect('div.federal-member') 
for div in federalmember:
    data = {}
    data['member'] = div.cssselect("div.federal-member-name")[0].text
    data['description'] = div.cssselect("div.federal-member-description")[0].text
    data['position'] = div.cssselect("div.federal-member-position")[0].text
    print data
    scraperwiki.sqlite.save(unique_keys=["member"], data=data)
        ###############################################################################
# START HERE: Tutorial 2: Basic scraping and saving to the data store.
# Follow the actions listed in BLOCK CAPITALS below.
###############################################################################

import scraperwiki
html = scraperwiki.scrape('http://www.australianmarriageequality.com/whereyourmpstands/states/NSW/')


import lxml.html
root = lxml.html.fromstring(html) 
federalmember = root.cssselect('div.federal-member') 
for div in federalmember:
    data = {}
    data['member'] = div.cssselect("div.federal-member-name")[0].text
    data['description'] = div.cssselect("div.federal-member-description")[0].text
    data['position'] = div.cssselect("div.federal-member-position")[0].text
    print data
    scraperwiki.sqlite.save(unique_keys=["member"], data=data)
        