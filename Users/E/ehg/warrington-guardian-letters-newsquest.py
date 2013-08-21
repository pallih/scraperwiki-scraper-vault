###############################################################################
# Initial scraper for Newsquest sites' letters
# Version: 0.1
# TODO: Do not scrape previously scraped letter URLs
# TODO: Fix body formatting
###############################################################################

import scraperwiki
import re
import time
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
from datetime import datetime


def scrape_letter(link):
    html = scraperwiki.scrape(link)
    
    html = re.sub('<!-- Actual Article Text Start -->', "<div id='article-body'>", html)
    html = re.sub('<!-- Actual Article Text End -->', "</div>", html)
    
    soup = BeautifulSoup(html)
    
    article = soup.find('div', { 'class' : 'sglCol article' })


    title = article.find('h3').text  
    date = article.find('p', { 'class' : 'articlePublished' }).text
    
    body = ''
    bodyparts = article.find('div', { "id" : "article-body"}).findAll(text = True)
    
    for part in bodyparts:
        body += part
    
    print body
    
    # Clean date
    date = re.sub(r"(\w+ \d+)\w+ (\w+ \d+)", "\\1 \\2", date)
    date = re.sub(r"(^[1-9]:)", "0\\1", date)
    dateTuple = time.strptime(date, "%I:%M%p %A %d %B %Y")
    
    record = {}
    record['title'] = title
    record['body'] = body
    
    scraperwiki.metadata.save(link, "scraped") # For some reason this doesn't work?
    scraperwiki.datastore.save(['title'], record, datetime(*dateTuple[:6])) 
    

# Iterate through paged letter list
def scrape_list_of_letters(url):
    html = scraperwiki.scrape(url.geturl())
    soup = BeautifulSoup(html)
    divs = soup.find('div', {'class' : 'sglCol'})
    for div in divs:
        header = div.find('h2')
    
        if header is None:
            header = div.find('h3')
    
        if header is not None and header != -1:
            link = header.findAll('a')[-1]
            if link is not None:
                moreLink = None
                
                next_url = url.scheme + '://' + url.netloc + link['href']
                print next_url
                print link.text
            
                if re.search(u"\u00BB", link.text) is not None:
                    scrape_list_of_letters(urlparse(next_url))
                elif re.search(u"\u00AB", link.text) is not None:
                    break
                elif scraperwiki.metadata.get(next_url) is not None:
                    print "scraped previous, skipping " + next_url
                    continue
                else:                
                    scrape_letter(next_url)
                
#################### START ######################           

scrape_list_of_letters(urlparse('http://www.warringtonguardian.co.uk/yoursay/letters'))

    