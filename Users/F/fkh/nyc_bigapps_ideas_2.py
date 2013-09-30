#thanks to the scraperwiki documentation for the bones of this script.


import scraperwiki
import lxml.html
import urlparse

#do the actual scraping
def scrape_block(root):
    lis = root.cssselect('li.item_content') # get all the <li> tags
    for li in lis:
        record = {}

        # this is the description of the idea
        record['Idea'] =  li.cssselect('h4')[0].text_content().replace("I want an NYC app that ","") 

        # this is count of comments
        c =  li.cssselect('a')[1].text_content()
        c = c.replace(" comments","")
        c = c.replace(" comment","")
        record['Comments'] = c

        # this is the submission date
        d = li.cssselect('p.subtitle')[0].text_content()
        d = d.partition("|")[2]
        record['Ago'] = d.split()[0]

        # this is the user-assigned category
        record['Category'] =  li.cssselect('a')[2].text_content()

        # who suggested it
        # sometimes who is blank, I don't know a more elegant way to avoid this prob
        who = 'Unknown'
        if li.cssselect('a.user-profile-link'):        
            who = li.cssselect('a.user-profile-link')[0].text_content()
        
        record['Who'] = who
            
        scraperwiki.sqlite.save(['Idea'], record)

# go through the pages
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)    
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object

    #send this off to be scraped
    scrape_block(root)

    # now find the next url
    next_link = root.cssselect("a.next_page")
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        scrape_and_look_for_next_link(next_url)

# starting point...
base_url = 'http://ideas.nycbigapps.com/'
starting_url = urlparse.urljoin(base_url, '?page=1')
scrape_and_look_for_next_link(starting_url)
#thanks to the scraperwiki documentation for the bones of this script.


import scraperwiki
import lxml.html
import urlparse

#do the actual scraping
def scrape_block(root):
    lis = root.cssselect('li.item_content') # get all the <li> tags
    for li in lis:
        record = {}

        # this is the description of the idea
        record['Idea'] =  li.cssselect('h4')[0].text_content().replace("I want an NYC app that ","") 

        # this is count of comments
        c =  li.cssselect('a')[1].text_content()
        c = c.replace(" comments","")
        c = c.replace(" comment","")
        record['Comments'] = c

        # this is the submission date
        d = li.cssselect('p.subtitle')[0].text_content()
        d = d.partition("|")[2]
        record['Ago'] = d.split()[0]

        # this is the user-assigned category
        record['Category'] =  li.cssselect('a')[2].text_content()

        # who suggested it
        # sometimes who is blank, I don't know a more elegant way to avoid this prob
        who = 'Unknown'
        if li.cssselect('a.user-profile-link'):        
            who = li.cssselect('a.user-profile-link')[0].text_content()
        
        record['Who'] = who
            
        scraperwiki.sqlite.save(['Idea'], record)

# go through the pages
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)    
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object

    #send this off to be scraped
    scrape_block(root)

    # now find the next url
    next_link = root.cssselect("a.next_page")
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        scrape_and_look_for_next_link(next_url)

# starting point...
base_url = 'http://ideas.nycbigapps.com/'
starting_url = urlparse.urljoin(base_url, '?page=1')
scrape_and_look_for_next_link(starting_url)
