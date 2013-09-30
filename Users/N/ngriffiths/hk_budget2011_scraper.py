###############################################################################
# HK Gov Press Release Scraper
###############################################################################

import string
import scraperwiki
from BeautifulSoup import BeautifulSoup


### Functions:
# Function to get the text from the first <p> tag & clean it
def scrapeSpeech(url):
#    print 'scrapeSpeech URL:', url
    p = soup.p
    ''.join(soup.findAll(text=True))
    try:
        soup.find(text='(To be continued)').replaceWith(' ')
    except:
        print 'Text not found'
    try:
        soup.replace('&nbsp;',' ')
    except:
        print '&nbsp not found'
    print p


    record = { "p" : p.text }
    # Save records to the datastore
    scraperwiki.datastore.save(["p"], record)



# Starting URL
start_url = 'http://www.info.gov.hk/gia/general/201102/23/P201102230128.htm'


### Script Action:


# Retrieve the first page
html = scraperwiki.scrape(start_url)
#print html
soup = BeautifulSoup(html)

# Run the scraper on the first page
scrapeSpeech(html)

# Find the section of the page that contains links to the remained of the transcript
start=soup.find(alt='Related links')
#print "Start here:", start

# This sets the first link to look for
index = 2
# Check each item in the list for links to the next page of speech
for li in start.findAllNext('li'):
    link_title = li.a.text
#    print 'Link Title is:', link_title
    line = []
    li_num=str(index)
    next_link = 'Budget Speech by the Financial Secretary ('+li_num+')'
#    print 'Next Link:', next_link

    # Check that the links are for the Budget Speech & if so, pull the URL
    for a in li.findAll('a'):
        href = str(a.get('href'))
#        print 'URL is: ' + href
        scrape_url = href
#        print 'Preparing to scrape:', scrape_url

            
        if next_link == link_title:
            # Retrieve the page
            scrape_url = href
#            print 'pullPage scrape_url value:', scrape_url
            html = scraperwiki.scrape(scrape_url)
#            print 'pullPage html value:', html
            soup = BeautifulSoup(html)
#            print 'pullPage soup value:', soup
 
            # Pull the text & clean it
            scrapeSpeech(html)
            index = index + 1
        # Append the text to the file
        
        else:
            print 'Links do not match. Ignoring...'
            exit


###############################################################################
# HK Gov Press Release Scraper
###############################################################################

import string
import scraperwiki
from BeautifulSoup import BeautifulSoup


### Functions:
# Function to get the text from the first <p> tag & clean it
def scrapeSpeech(url):
#    print 'scrapeSpeech URL:', url
    p = soup.p
    ''.join(soup.findAll(text=True))
    try:
        soup.find(text='(To be continued)').replaceWith(' ')
    except:
        print 'Text not found'
    try:
        soup.replace('&nbsp;',' ')
    except:
        print '&nbsp not found'
    print p


    record = { "p" : p.text }
    # Save records to the datastore
    scraperwiki.datastore.save(["p"], record)



# Starting URL
start_url = 'http://www.info.gov.hk/gia/general/201102/23/P201102230128.htm'


### Script Action:


# Retrieve the first page
html = scraperwiki.scrape(start_url)
#print html
soup = BeautifulSoup(html)

# Run the scraper on the first page
scrapeSpeech(html)

# Find the section of the page that contains links to the remained of the transcript
start=soup.find(alt='Related links')
#print "Start here:", start

# This sets the first link to look for
index = 2
# Check each item in the list for links to the next page of speech
for li in start.findAllNext('li'):
    link_title = li.a.text
#    print 'Link Title is:', link_title
    line = []
    li_num=str(index)
    next_link = 'Budget Speech by the Financial Secretary ('+li_num+')'
#    print 'Next Link:', next_link

    # Check that the links are for the Budget Speech & if so, pull the URL
    for a in li.findAll('a'):
        href = str(a.get('href'))
#        print 'URL is: ' + href
        scrape_url = href
#        print 'Preparing to scrape:', scrape_url

            
        if next_link == link_title:
            # Retrieve the page
            scrape_url = href
#            print 'pullPage scrape_url value:', scrape_url
            html = scraperwiki.scrape(scrape_url)
#            print 'pullPage html value:', html
            soup = BeautifulSoup(html)
#            print 'pullPage soup value:', soup
 
            # Pull the text & clean it
            scrapeSpeech(html)
            index = index + 1
        # Append the text to the file
        
        else:
            print 'Links do not match. Ignoring...'
            exit


