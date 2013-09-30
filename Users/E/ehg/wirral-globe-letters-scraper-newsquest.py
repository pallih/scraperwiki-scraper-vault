###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse

def scrape_letter(link):
    html = scraperwiki.scrape(link)
    
    html = re.sub('<!-- Actual Article Text Start -->', "<div id='article-body'>", html)
    html = re.sub('<!-- Actual Article Text End -->', "</div>", html)
    
    print html
    soup = BeautifulSoup(html)
    

    print soup
    
    article = soup.find('div', { 'class' : 'sglCol article' })


    title = article.find('h3').text  
    date = article.find('p', { 'class' : 'articlePublished' })
    
    #TODO: comments
    
    body = article.find('div', { "id" : "article-body")
    
    print title
    print body
    
    
    #record = { "td" : td.text }
    # save records to the datastore
    #scraperwiki.datastore.save(["td"], record) 


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
            
                if re.search('More Letters', link.text) is not None:
                    scrape_list_of_letters(urlparse(next_url))
                elif re.search('Back', link.text) is not None:
                    break
                else:                
                    scrape_letter(next_url)
                
########## start###########            

scrape_list_of_letters(urlparse('http://www.wirralglobe.co.uk/yoursay/wirralletters'))
###############################################################################
# Basic scraper
###############################################################################

import scraperwiki
import re
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse

def scrape_letter(link):
    html = scraperwiki.scrape(link)
    
    html = re.sub('<!-- Actual Article Text Start -->', "<div id='article-body'>", html)
    html = re.sub('<!-- Actual Article Text End -->', "</div>", html)
    
    print html
    soup = BeautifulSoup(html)
    

    print soup
    
    article = soup.find('div', { 'class' : 'sglCol article' })


    title = article.find('h3').text  
    date = article.find('p', { 'class' : 'articlePublished' })
    
    #TODO: comments
    
    body = article.find('div', { "id" : "article-body")
    
    print title
    print body
    
    
    #record = { "td" : td.text }
    # save records to the datastore
    #scraperwiki.datastore.save(["td"], record) 


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
            
                if re.search('More Letters', link.text) is not None:
                    scrape_list_of_letters(urlparse(next_url))
                elif re.search('Back', link.text) is not None:
                    break
                else:                
                    scrape_letter(next_url)
                
########## start###########            

scrape_list_of_letters(urlparse('http://www.wirralglobe.co.uk/yoursay/wirralletters'))
