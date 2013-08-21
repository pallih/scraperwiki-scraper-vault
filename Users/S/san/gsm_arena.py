# Scrapes phone info from GSM Arena webpage

import scraperwiki
import lxml.html
import re # http://docs.python.org/2/library/re.html
from urlparse import urlparse

# Get root node from url
def scrape_content(url):
    html = scraperwiki.scrape(url)
    return lxml.html.fromstring(html)

# Get image from the pictures page
def get_img(src, url):
    # create url of pics page from spec page
    root = scrape_content('http://' + urlparse(url).netloc + '/' + src)
    # retrieve image url and return
    return root.cssselect('div#pictures img')[0].attrib['src'] 

# Parse Phone Details
def scrape_phone(url):
    global counter
    phone = dict()
    root = scrape_content(url)
    # Get the spec tables
    el = root.cssselect('div#specs-list table')    
    # Display table
    display = el[2]
    disp = display.cssselect('td')[3].text_content()
    # regex for contents within parantheses ()
    phone['density'] = re.search('\((.*)\)', disp).group(1)
    # regex for size 2.8 inches or 3.0 inches
    phone['size'] = re.search('\d*\.?\d\sinches', disp).group(0)
    # regex for dimensions like 200 x 300
    phone['dimension'] = re.search('\d*\sx\s\d*', disp).group(0)
    # Features table
    features = el[7]
    phone['os'] = features.cssselect('td')[1].text_content()
    phone['link'] = url
    phone['img'] = get_img(root.cssselect('div#specs-cp-pic a')[0].attrib['href'], url)
    phone['id'] = counter    
    print scraperwiki.sqlite.save(unique_keys=['id'], data=phone)
    counter += 1

# Records counter, used as ID in records
counter = 1

src = 'http://www.gsmarena.com/htc_merge-3739.php'
scrape_phone(src)
src = 'http://www.gsmarena.com/motorola_razr_i_xt890-4998.php'
scrape_phone(src)
src = 'http://www.gsmarena.com/motorola_droid_razr_maxx_hd-4972.php'
scrape_phone(src)
src = 'http://www.gsmarena.com/motorola_photon_q_4g_lte_xt897-4885.php'
scrape_phone(src)