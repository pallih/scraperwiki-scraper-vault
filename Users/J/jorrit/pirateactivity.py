import scraperwiki

# -*- coding: utf-8 -*- 

import urllib2
 
from bs4 import BeautifulSoup

proxy_handler = urllib2.ProxyHandler({'http': 'http://proxy-eu.shell.com:8080'})
opener = urllib2.build_opener(proxy_handler)
urllib2.install_opener(opener)

def dosoup(soup):
    for a in soup.find_all("a", "fabrik___rowlink"):
        link = a.get('href')
        url = 'http://' + host + link
        #print url
        
        fh = urllib2.urlopen(url)
        html = fh.read()
        fh.close
        
        cupasoup = BeautifulSoup(html)
        for div in cupasoup.find_all("div", "fabrikElement"):
            #print 'div ' + str(div)
            if div.find('div', id="jos_fabrik_icc_ccs_piracymap2012___attack_position_map_ro"):
                div2 = div.find('div', id="jos_fabrik_icc_ccs_piracymap2012___attack_position_map_ro")
                lat = div2.find('span', 'latitude').text
                lon = div2.find('span', 'longitude').text
                #print 'lat ' + lat
                #print 'lon ' + lon
            
        #print '%s,%s,%s' % (url, lat, lon)
        scraperwiki.sqlite.save(unique_keys=["URL"], data={"URL":url, "LAT":lat, "LON":lon})
    
host = 'www.icc-ccs.org'

url = 'http://' + host + '/piracy-reporting-centre/live-piracy-report'
fh = urllib2.urlopen(url)

html = fh.read()
fh.close

soup = BeautifulSoup(html)

dosoup(soup)

