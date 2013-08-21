# PLEASE READ THIS BEFORE EDITING
#
# This script generates your email alerts, to tell you when your scrapers
# are broken or someone has edited them.
#
# It works by emailing you the output of this script. If you read the code and
# know what you're doing, you can customise it, and make it send other emails
# for other purposes.

import scraperwiki
import urllib2
import urllib
import lxml.html
import BeautifulSoup as bs
import re    
import xml.etree.ElementTree as ET

for i in range(615, 2000):
    url ='http://www.dlapiper.com/us/people/detail.aspx?attorney='+str(i)
    try:           
        page = scraperwiki.scrape(url)
        html = bs.BeautifulSoup(page)
        lawer_name = html.findAll('h1')
        lawer_post = html.findAll('h2')
        root = lxml.html.fromstring(page)
        links = root.cssselect("div.bio a")
        contact = root.cssselect("div.bio td")
        data = {'name':lawer_name[4].getText(), 'post' : lawer_post[3].getText(), 'email' : links[0].text, 'contact':contact[0].text_content(),'id':i}
        scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    except:
        pass
                                
    
    
    
    

