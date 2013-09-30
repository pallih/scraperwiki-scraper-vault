# List of all universities in the world, along with their country code and URL

# Copied from Jo Walsh' list of 12000, simply without a limit and with some code to scrape the country code.

offset = 0
from time import sleep

# links look like this
# <a href="http://www.upenn.edu/" target="_blank"  class="nav6a">

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.webometrics.info/top12000.asp?offset='


def one_page(url):
    html = None
    # sleep(1)
    print url
    try: 
        html = scraperwiki.scrape(url)

    except:
        return 

    soup = BeautifulSoup(html)
    next = 0;    
    # use BeautifulSoup to get all <a...> tags
    links = soup.findAll('a')
    for a in links:
        if a.text != 'First' and a.text != 'Next' and a.text != 'Previous' and a.text != 'Last':
            if a.has_key('class') and a['class'] == 'nav6a':
                #Grab the alt text for the flag image - this is where we get the country code from
                country = a.parent.nextSibling.next.contents[1]['alt'].split()[-1]
                scraperwiki.sqlite.save(['href'],{'name':a.text,'country':country,'href':a['href']})

        if a.text == 'Next':
            next = 1
    return next

print starting_url
offset = 0
while( offset <= 20350  ):
    one_page(starting_url+str(offset))
    print 'Next page'

# List of all universities in the world, along with their country code and URL

# Copied from Jo Walsh' list of 12000, simply without a limit and with some code to scrape the country code.

offset = 0
from time import sleep

# links look like this
# <a href="http://www.upenn.edu/" target="_blank"  class="nav6a">

import scraperwiki
from BeautifulSoup import BeautifulSoup

# retrieve a page
starting_url = 'http://www.webometrics.info/top12000.asp?offset='


def one_page(url):
    html = None
    # sleep(1)
    print url
    try: 
        html = scraperwiki.scrape(url)

    except:
        return 

    soup = BeautifulSoup(html)
    next = 0;    
    # use BeautifulSoup to get all <a...> tags
    links = soup.findAll('a')
    for a in links:
        if a.text != 'First' and a.text != 'Next' and a.text != 'Previous' and a.text != 'Last':
            if a.has_key('class') and a['class'] == 'nav6a':
                #Grab the alt text for the flag image - this is where we get the country code from
                country = a.parent.nextSibling.next.contents[1]['alt'].split()[-1]
                scraperwiki.sqlite.save(['href'],{'name':a.text,'country':country,'href':a['href']})

        if a.text == 'Next':
            next = 1
    return next

print starting_url
offset = 0
while( offset <= 20350  ):
    one_page(starting_url+str(offset))
    print 'Next page'

