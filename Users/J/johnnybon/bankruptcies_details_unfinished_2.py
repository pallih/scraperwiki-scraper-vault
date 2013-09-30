#Find link to each details page
#Scrape the contents of the page at that link
#Return to search results and repeat
#Then go to 'next' link

#http://www.london-gazette.co.uk/issues/recent/10/personal-insolvency/bankruptcy/start=1
#HTML:
#<div id="divResult" class="Result">
#<dl class="Details">
# <dt class="PubDate">Date:</dt>
# <dd class="PubDate">
#<p class="summary">
# <strong class="highlight">60112</strong> 
#<ul class="Links">                       
# <li class="lteIE6_first-child" about="http://www.london-gazette.co.uk/id/issues/60112" typeof="g:Issue" property="g:hasPublicationDate" content="2012-04-10" rel="g:hasNotice"><a href="/issues/60112/notices/1568613/recent=10;category=personal-insolvency;subcategory=bankruptcy" about="http://www.london-gazette.co.uk/id/issues/60112/notices/1568613" typeof="g:Notice"><img alt="See full notice" title="See full notice" src="/styles/styleimages/button_seeFullNotice.gif" /></a></li>
# <li about="http://www.london-gazette.co.uk/id/issues/60112/notices/1568613" typeof="g:Notice" rel="foaf:page"><a target="_blank" href="/issues/60112/pages/6994" typeof="foaf:Document"><img alt="See PDF" title="See PDF" src="/styles/styleimages/button_seePDF.gif" /></a></li><li><a target='_blank' href='https://www.tsoshop.co.uk/bookstore.asp?FO=1159966&amp;Action=AddItem&amp;ExternalRef=60112'>

import scraperwiki
import urlparse
import lxml.html

def scrape_page(root):
    print root
    divdata = root.cssselect("div.Data") #data is in <div class="Data"><div><p>
    for pars in divdata:
        #Create a new empty record
        record = {}
        #Assign the contents of <p> to a new object (list) called 'lines'
        lines = pars.cssselect("p")
        #And the contents of <p><span> to 'spans' object (list)
        spans = pars.cssselect("p span")
        #If there's anything
        if lines: 
            #Put the contents of the first <p> into a record in the column 'pubdate'
            record['pubdate'] = spans[0].text
            record['noticecode'] = spans[1].text
            record['name'] = spans[2].text
            record['address'] = lines[4].text
            record['DOB'] = lines[5].text
            record['description'] = lines[6].text
            record['court'] = lines[7].text
            record['dateofpetition'] = lines[8].text
            record['dateoforder'] = lines[9].text
            record['timeoforder'] = lines[10].text
            record['petitionby'] = lines[11].text
            record['receiver'] = spans[3].text
#            record['date'] = lines[13].text #in one entry this breaks the scraper
#            record['urlcode'] = lines[14].text #in one entry this breaks the scraper
            print record, '------------'
            #Save in the SQLite database, with the ID code to be used as the unique reference
            scraperwiki.sqlite.save(["DOB"], record)
    

# scrape_table function: gets passed an individual page to scrape
def scrape_links(root):
    links = root.cssselect("div.Result a")  # selects all <a> links in <div class="Result">
    for link in links:
        aboutattr = link.attrib.get('about')
        print aboutattr
        if not aboutattr: continue
        html = scraperwiki.scrape(aboutattr)
        print html
        linkedpage = lxml.html.fromstring(html)
        scrape_page(linkedpage)
        # Set up data record
#        record = {}
 #       aboutattr = link.attrib.get('about')
  #      if aboutattr:
   #         record['link'] = aboutattr
    #        print record, '------------'
     #       scraperwiki.sqlite.save(["link"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_links(root)
    next_link = root.cssselect("a.Next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# START HERE: define your starting URL - then 
base_url = 'http://www.london-gazette.co.uk'
starting_url = urlparse.urljoin(base_url, '/issues/recent/10/personal-insolvency/bankruptcy/start=1')
scrape_and_look_for_next_link(starting_url)
#Find link to each details page
#Scrape the contents of the page at that link
#Return to search results and repeat
#Then go to 'next' link

#http://www.london-gazette.co.uk/issues/recent/10/personal-insolvency/bankruptcy/start=1
#HTML:
#<div id="divResult" class="Result">
#<dl class="Details">
# <dt class="PubDate">Date:</dt>
# <dd class="PubDate">
#<p class="summary">
# <strong class="highlight">60112</strong> 
#<ul class="Links">                       
# <li class="lteIE6_first-child" about="http://www.london-gazette.co.uk/id/issues/60112" typeof="g:Issue" property="g:hasPublicationDate" content="2012-04-10" rel="g:hasNotice"><a href="/issues/60112/notices/1568613/recent=10;category=personal-insolvency;subcategory=bankruptcy" about="http://www.london-gazette.co.uk/id/issues/60112/notices/1568613" typeof="g:Notice"><img alt="See full notice" title="See full notice" src="/styles/styleimages/button_seeFullNotice.gif" /></a></li>
# <li about="http://www.london-gazette.co.uk/id/issues/60112/notices/1568613" typeof="g:Notice" rel="foaf:page"><a target="_blank" href="/issues/60112/pages/6994" typeof="foaf:Document"><img alt="See PDF" title="See PDF" src="/styles/styleimages/button_seePDF.gif" /></a></li><li><a target='_blank' href='https://www.tsoshop.co.uk/bookstore.asp?FO=1159966&amp;Action=AddItem&amp;ExternalRef=60112'>

import scraperwiki
import urlparse
import lxml.html

def scrape_page(root):
    print root
    divdata = root.cssselect("div.Data") #data is in <div class="Data"><div><p>
    for pars in divdata:
        #Create a new empty record
        record = {}
        #Assign the contents of <p> to a new object (list) called 'lines'
        lines = pars.cssselect("p")
        #And the contents of <p><span> to 'spans' object (list)
        spans = pars.cssselect("p span")
        #If there's anything
        if lines: 
            #Put the contents of the first <p> into a record in the column 'pubdate'
            record['pubdate'] = spans[0].text
            record['noticecode'] = spans[1].text
            record['name'] = spans[2].text
            record['address'] = lines[4].text
            record['DOB'] = lines[5].text
            record['description'] = lines[6].text
            record['court'] = lines[7].text
            record['dateofpetition'] = lines[8].text
            record['dateoforder'] = lines[9].text
            record['timeoforder'] = lines[10].text
            record['petitionby'] = lines[11].text
            record['receiver'] = spans[3].text
#            record['date'] = lines[13].text #in one entry this breaks the scraper
#            record['urlcode'] = lines[14].text #in one entry this breaks the scraper
            print record, '------------'
            #Save in the SQLite database, with the ID code to be used as the unique reference
            scraperwiki.sqlite.save(["DOB"], record)
    

# scrape_table function: gets passed an individual page to scrape
def scrape_links(root):
    links = root.cssselect("div.Result a")  # selects all <a> links in <div class="Result">
    for link in links:
        aboutattr = link.attrib.get('about')
        print aboutattr
        if not aboutattr: continue
        html = scraperwiki.scrape(aboutattr)
        print html
        linkedpage = lxml.html.fromstring(html)
        scrape_page(linkedpage)
        # Set up data record
#        record = {}
 #       aboutattr = link.attrib.get('about')
  #      if aboutattr:
   #         record['link'] = aboutattr
    #        print record, '------------'
     #       scraperwiki.sqlite.save(["link"], record)
        
# scrape_and_look_for_next_link function: calls the scrape_table
# function, then hunts for a 'next' link: if one is found, calls itself again
def scrape_and_look_for_next_link(url):
    html = scraperwiki.scrape(url)
    print html
    root = lxml.html.fromstring(html)
    scrape_links(root)
    next_link = root.cssselect("a.Next")
    print next_link
    if next_link:
        next_url = urlparse.urljoin(base_url, next_link[0].attrib.get('href'))
        print next_url
        scrape_and_look_for_next_link(next_url)

# START HERE: define your starting URL - then 
base_url = 'http://www.london-gazette.co.uk'
starting_url = urlparse.urljoin(base_url, '/issues/recent/10/personal-insolvency/bankruptcy/start=1')
scrape_and_look_for_next_link(starting_url)
