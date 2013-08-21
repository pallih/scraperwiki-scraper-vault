import scraperwiki
import json
import re
import urlparse
import lxml.html
import time

def getTextFromXpath(refelement,xpath_str):
    value = ''
    el = refelement.xpath(xpath_str)
    if len(el) > 0:
        value = el[0].text
    return value

def scrape_listingContent(listingContent):
    dataLid=listingContent.xpath('.//h3[@class="business-name fn org"]')[0].attrib['data-lid']
    title = listingContent.xpath('.//h3[@class="business-name fn org"]//a')[0].text     
    streetAddress = getTextFromXpath(listingContent,'.//span[@class="street-address"]')
    locality =  getTextFromXpath(listingContent,'.//span[@class="locality"]')
    region =  getTextFromXpath(listingContent,'.//span[@class="region"]')
    postalCode =  getTextFromXpath(listingContent,'.//span[@class="postal-code"]')
    phone = getTextFromXpath(listingContent,'.//span[@class="business-phone phone"]')
    localtime = time.asctime( time.localtime(time.time()) )

    data = {}
    data['dataLid'] = dataLid
    data['title'] = title
    data['streetAddress'] = streetAddress
    data['locality'] = locality
    data['region'] = region
    data['postalCode'] = postalCode
    data['phone'] = phone
    data['Extracted_Time'] = localtime
    scraperwiki.sqlite.save(['dataLid'],data)

    print title

yp_url = []
yp_url.append('http://www.yellowpages.com/07747/doctors')
yp_url.append('http://www.yellowpages.com/14221/doctors')

for url in yp_url:
    start = 0
    pageurl = url
    while (start >= 0):
        print pageurl
        html= scraperwiki.scrape(pageurl)
        tree = lxml.html.fromstring(html)

        for listingContent in tree.xpath('//div[@class="listing_content"]'):
            scrape_listingContent(listingContent)
        
        pagnext = tree.xpath('//li[@class="next"]//a')
        if pagnext is not None:
            pageurl = 'http://www.yellowpages.com' + pagnext[0].get('href','')
            start += 1
        else:
            start = -1

