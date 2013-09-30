###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next'
# links from page to page: use functions, so you can call the same code
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import urllib2
import urllib
import cookielib

#  The code will install a set of specific handlers to be used when a URL
#  is opened. See the "urllibSetup" and "urllib2Setup" functions below.
#
urllibopener  = None
urllib2cj     = None
urllib2opener = None

#  The "urllib2Setup" function is called with zero or more handlers. An opener
#  is constructed using these, plus a cookie processor, and is installed as the
#  urllib2 opener. The opener also overrides the user-agent header.
#
def urllib2Setup (*handlers) :

    global urllib2cj
    global urllib2opener
    urllib2cj = cookielib.CookieJar()
    urllib2opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(urllib2cj), *handlers)
    urllib2opener.addheaders = [('User-agent', 'ScraperWiki')]
    urllib2.install_opener (urllib2opener)

#  Similarly for urllib, but no handlers.
#
def urllibSetup () :

    global urllibopener
    urllibopener = urllib.URLopener()
    urllibopener.addheaders = [('User-agent', 'ScraperWiki')]
    urllib._urlopener = urllibopener


#  Scrape a URL optionally with parameters. This is effectively a wrapper around
#  urllib2.orlopen().
#
def scrape (url, params = None) :

    #  Normally the "urllib2Setup" function would have been called from
    #  the controller to specify http, https and ftp proxies, however check
    #  in case not and call without any handlers.
    #
    global urllib2opener
    if urllib2opener is None :
        urllib2Setup ()

    data = params and urllib.urlencode(params) or None

    fin  = urllib2opener.open(url, data)
    text = fin.read()
    fin.close()   # get the mimetype here

    return text


# scrape_table function: gets passed an individual page to scrape
def scrape_table(id, root):
    # Hint: xpath from Firebg without tbody elements
    element = root.xpath('/html/body/div[2]/div[2]/div/table/tr[3]/td/div/table/tr/td[2]/h1')
    if not element: return
    serie = element[0].text # Serienname
    table= root.xpath('/html/body/div[2]/div[2]/div/table/tr[3]/td/div/table[2]/tr/td[2]/table') # Sendetermine
    trs = table and table[0].cssselect('tr') # get all the <tr> tags
    data = []
    episode = {}
    for tr in trs:
        episode ['ID'] = id
        element = tr.xpath('td[1]/p/nobr')
        if not element: continue
        episode ['Tag'] = element[0].text # Sendetag
        element = tr.xpath('td[2]/p/nobr')
        if not element: continue
        episode ['Datum'] = element[0].text # Sendedatum
        element = tr.xpath('td[3]/p/nobr')
        if not element: continue
        episode ['Uhrzeit'] = element[0].text # Sendeuhrzeit
        element = tr.xpath('td[4]/p/nobr')
        if not element: continue
        episode ['Sender'] = element[0].text # Sender
        episode ['Serie'] = serie # Serie
        element = tr.xpath('td[5]/p/nobr/a')
        if not element: continue
        episode ['Nummer'] = element[0].text # Episodenummer
        element = tr.xpath('td[6]/p')
        if not element: continue
        episode ['Titel'] = element[0].text # Episodename
        # For debugging: Print out the data we've gathered
        #print episode 
        data.append( episode )
    # Finally, save the episode to the datastore - 'Fernsehserien' is our unique key
    scraperwiki.sqlite.save(['ID','Datum','Uhrzeit','Sender'], data)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(id, url):
    html = scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(id, root) #
    next_link = root.xpath('//a[starts-with(text(), "weiterbl")]/@href')
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0])
        scrape_and_look_for_next_link(id, next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.fernsehserien.de/'

#for serie in [1,100]:
for serie in xrange(1,100):
    for seite in [6,8]:
        #Serienids: dr. house 1127 hustle 44 castle 13468
        #Sender: ZDF 2 ZDF_NEO 178 RTL 28 KABEL1 19

        # Past events "Seite=6"
        # Future events "Seite=8"
        #starting_url = urlparse.urljoin(base_url, 'index.php?serie=1127&seite=6&sender=&start=-1') 
        starting_url = urlparse.urljoin(base_url, 'index.php?serie=%d&seite=%d&sender=&start=-1' % (serie,seite) ) 

        scrape_and_look_for_next_link(serie, starting_url)

###############################################################################
# START HERE: Tutorial 3: More advanced scraping. Shows how to follow 'next'
# links from page to page: use functions, so you can call the same code
# repeatedly. SCROLL TO THE BOTTOM TO SEE THE START OF THE SCRAPER.
###############################################################################

import scraperwiki
import urlparse
import lxml.html
import urllib2
import urllib
import cookielib

#  The code will install a set of specific handlers to be used when a URL
#  is opened. See the "urllibSetup" and "urllib2Setup" functions below.
#
urllibopener  = None
urllib2cj     = None
urllib2opener = None

#  The "urllib2Setup" function is called with zero or more handlers. An opener
#  is constructed using these, plus a cookie processor, and is installed as the
#  urllib2 opener. The opener also overrides the user-agent header.
#
def urllib2Setup (*handlers) :

    global urllib2cj
    global urllib2opener
    urllib2cj = cookielib.CookieJar()
    urllib2opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(urllib2cj), *handlers)
    urllib2opener.addheaders = [('User-agent', 'ScraperWiki')]
    urllib2.install_opener (urllib2opener)

#  Similarly for urllib, but no handlers.
#
def urllibSetup () :

    global urllibopener
    urllibopener = urllib.URLopener()
    urllibopener.addheaders = [('User-agent', 'ScraperWiki')]
    urllib._urlopener = urllibopener


#  Scrape a URL optionally with parameters. This is effectively a wrapper around
#  urllib2.orlopen().
#
def scrape (url, params = None) :

    #  Normally the "urllib2Setup" function would have been called from
    #  the controller to specify http, https and ftp proxies, however check
    #  in case not and call without any handlers.
    #
    global urllib2opener
    if urllib2opener is None :
        urllib2Setup ()

    data = params and urllib.urlencode(params) or None

    fin  = urllib2opener.open(url, data)
    text = fin.read()
    fin.close()   # get the mimetype here

    return text


# scrape_table function: gets passed an individual page to scrape
def scrape_table(id, root):
    # Hint: xpath from Firebg without tbody elements
    element = root.xpath('/html/body/div[2]/div[2]/div/table/tr[3]/td/div/table/tr/td[2]/h1')
    if not element: return
    serie = element[0].text # Serienname
    table= root.xpath('/html/body/div[2]/div[2]/div/table/tr[3]/td/div/table[2]/tr/td[2]/table') # Sendetermine
    trs = table and table[0].cssselect('tr') # get all the <tr> tags
    data = []
    episode = {}
    for tr in trs:
        episode ['ID'] = id
        element = tr.xpath('td[1]/p/nobr')
        if not element: continue
        episode ['Tag'] = element[0].text # Sendetag
        element = tr.xpath('td[2]/p/nobr')
        if not element: continue
        episode ['Datum'] = element[0].text # Sendedatum
        element = tr.xpath('td[3]/p/nobr')
        if not element: continue
        episode ['Uhrzeit'] = element[0].text # Sendeuhrzeit
        element = tr.xpath('td[4]/p/nobr')
        if not element: continue
        episode ['Sender'] = element[0].text # Sender
        episode ['Serie'] = serie # Serie
        element = tr.xpath('td[5]/p/nobr/a')
        if not element: continue
        episode ['Nummer'] = element[0].text # Episodenummer
        element = tr.xpath('td[6]/p')
        if not element: continue
        episode ['Titel'] = element[0].text # Episodename
        # For debugging: Print out the data we've gathered
        #print episode 
        data.append( episode )
    # Finally, save the episode to the datastore - 'Fernsehserien' is our unique key
    scraperwiki.sqlite.save(['ID','Datum','Uhrzeit','Sender'], data)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(id, url):
    html = scrape(url)
    root = lxml.html.fromstring(html)
    scrape_table(id, root) #
    next_link = root.xpath('//a[starts-with(text(), "weiterbl")]/@href')
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0])
        scrape_and_look_for_next_link(id, next_url)

# ---------------------------------------------------------------------------
# START HERE: define your starting URL - then
# call a function to scrape the first page in the series.
# ---------------------------------------------------------------------------
base_url = 'http://www.fernsehserien.de/'

#for serie in [1,100]:
for serie in xrange(1,100):
    for seite in [6,8]:
        #Serienids: dr. house 1127 hustle 44 castle 13468
        #Sender: ZDF 2 ZDF_NEO 178 RTL 28 KABEL1 19

        # Past events "Seite=6"
        # Future events "Seite=8"
        #starting_url = urlparse.urljoin(base_url, 'index.php?serie=1127&seite=6&sender=&start=-1') 
        starting_url = urlparse.urljoin(base_url, 'index.php?serie=%d&seite=%d&sender=&start=-1' % (serie,seite) ) 

        scrape_and_look_for_next_link(serie, starting_url)

