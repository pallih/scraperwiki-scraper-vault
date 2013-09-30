import scraperwiki
import lxml.html
import os
#import BeautifulSoup
import sys
import urlparse
import re

def get_papers():

    # there is a page for each state
    states = []
    top_url = "http://www.usnpl.com/"
 
    #html = scraperwiki.scrape( top_url )
    #doc = lxml.html.document_fromstring(html)
    #doc.make_links_absolute(top_url)
    doc = lxml.html.parse( top_url ).getroot()
    doc.make_links_absolute()
    box = doc.cssselect('#data_box')[0]

    for a in box.cssselect('a'):
        states.append( (a.text_content(), a.get('href')) )


    papers = []
    # for each state
    for s in states:
        print "------ %s -----" % ( s[0], )
        state_url = s[1]
        #html = scraperwiki.scrape( state_url )
        #doc = lxml.html.document_fromstring(html)
        #doc.make_links_absolute(state_url)
        doc = lxml.html.parse( state_url ).getroot()
        doc.make_links_absolute()
        for a in doc.cssselect( 'b + a' ):

            url = a.get('href')
            o = urlparse.urlparse( url )

            if o[1].lower() in ( 'www.usnpl.com','web.archive.org' ):
                continue

            papers.append( { 'name': a.text_content(),
                    'url': url,
                    'state': s[0] } )
    return papers

def main():

    papers = get_papers()
    for p in papers:
        scraperwiki.store( p )


main()

import scraperwiki
import lxml.html
import os
#import BeautifulSoup
import sys
import urlparse
import re

def get_papers():

    # there is a page for each state
    states = []
    top_url = "http://www.usnpl.com/"
 
    #html = scraperwiki.scrape( top_url )
    #doc = lxml.html.document_fromstring(html)
    #doc.make_links_absolute(top_url)
    doc = lxml.html.parse( top_url ).getroot()
    doc.make_links_absolute()
    box = doc.cssselect('#data_box')[0]

    for a in box.cssselect('a'):
        states.append( (a.text_content(), a.get('href')) )


    papers = []
    # for each state
    for s in states:
        print "------ %s -----" % ( s[0], )
        state_url = s[1]
        #html = scraperwiki.scrape( state_url )
        #doc = lxml.html.document_fromstring(html)
        #doc.make_links_absolute(state_url)
        doc = lxml.html.parse( state_url ).getroot()
        doc.make_links_absolute()
        for a in doc.cssselect( 'b + a' ):

            url = a.get('href')
            o = urlparse.urlparse( url )

            if o[1].lower() in ( 'www.usnpl.com','web.archive.org' ):
                continue

            papers.append( { 'name': a.text_content(),
                    'url': url,
                    'state': s[0] } )
    return papers

def main():

    papers = get_papers()
    for p in papers:
        scraperwiki.store( p )


main()

