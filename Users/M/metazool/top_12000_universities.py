# List of top 12000 Universities worldwide

# http://www.webometrics.info/top12000.asp 

# request pages stepping through offsets up to 12000 -  like this ?offset=50

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

    # use BeautifulSoup to get all <a...> tags
    links = soup.findAll('a')
    for a in links:
        if a.has_key('class') and a['class'] == 'nav6a':
            scraperwiki.sqlite.save(['href'],{'name':a.text,'href':a['href']})


while offset < 12000:
    print starting_url
    one_page(starting_url+str(offset))
    offset = offset+50

