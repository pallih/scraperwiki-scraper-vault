import scraperwiki

# Blank Python


#In each page puts contents of all <a> tags in <div class="Result"> into a list,
#Then loops through and puts the first 'about' attribute of each into a table
#Then finds 'next' link, and does the same for that linked page

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

# scrape_table function: gets passed an individual page to scrape
def scrape_links(root):
#    print root.cssselect("div.Result p"), 'AGHHH'
    links = root.cssselect("div.Result a")  # selects all <a> links in <div class="Result">
    for link in links:
        # Set up data record
        record = {}
        aboutattr = link.attrib.get('about')
        if aboutattr:
            record['link'] = aboutattr
            print record, '------------'
            scraperwiki.sqlite.save(["link"], record)
        
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
starting_url = urlparse.urljoin(base_url,'/issues/2012-05-01;2012-06-01/exact=appointment+of+administrators/start=1')
scrape_and_look_for_next_link(starting_url)