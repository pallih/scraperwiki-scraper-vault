###############################################################################
# Basic scraper
# Civic organizations
# Marek Sotak - http://twitter.com/sotak
# My second python script ever ;)
###############################################################################

import scraperwiki
import lxml.html

# starting_url = 'http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/SearchResult.aspx'
# pager http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/SearchResult.aspx?stranka=1

#i = scraperwiki.sqlite.get_var('last_id', 1)
i = 1;
# get the first 500 pages
for i in range(i, i+2):
    # retrieve a page
    # TODO: handle errors
    #starting_url = 'http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/Default.aspx'
    # starting_url = 'http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/SearchResult.aspx?stranka=' + str(i)
    starting_url ="http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/Default.aspx?__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTIxMTMyNDAyODZkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYFBTJjdGwwMCRjdGwwMCRBcHBsaWNhdGlvbiRCYXNlUGxhY2VIb2xkZXIkQ0JMX1N0YXYkMAUyY3RsMDAkY3RsMDAkQXBwbGljYXRpb24kQmFzZVBsYWNlSG9sZGVyJENCTF9TdGF2JDEFMmN0bDAwJGN0bDAwJEFwcGxpY2F0aW9uJEJhc2VQbGFjZUhvbGRlciRDQkxfU3RhdiQyBTJjdGwwMCRjdGwwMCRBcHBsaWNhdGlvbiRCYXNlUGxhY2VIb2xkZXIkQ0JMX1N0YXYkMwUyY3RsMDAkY3RsMDAkQXBwbGljYXRpb24kQmFzZVBsYWNlSG9sZGVyJENCTF9TdGF2JDNfhXwjJ2xPMtk9kY5c1D%2FfUZzR2g%3D%3D&ctl00%24ctl00%24Application%24BasePlaceHolder%24TB_nazev_Sdruzeni=&ctl00%24ctl00%24Application%24BasePlaceHolder%24Date1=&ctl00%24ctl00%24Application%24BasePlaceHolder%24Date2=&ctl00%24ctl00%24Application%24BasePlaceHolder%24TB_ICO=&ctl00%24ctl00%24Application%24BasePlaceHolder%24TB_Adresa=&ctl00%24ctl00%24Application%24BasePlaceHolder%24BTN_Show_All=Zobrazit+v%C5%A1echny&__EVENTVALIDATION=%2FwEWDALN0f7cCAKX76HUCgLy7eHFAgLy7eXFAgLy7dnFAgLy7d3FAgKOnqa5CQKRnqa5CQKTm4PtBgL8zswyAvqwxtYCAqSf58kItw06oX1W4ZhaWTWRQuaU7zA%2Fia8%3D";
    html = scraperwiki.scrape(starting_url)
    print html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("#searchResults tr"):
        tds = tr.cssselect("td")
        data = {
          'country' : tds[0].text_content()
        }
        print data
###############################################################################
# Basic scraper
# Civic organizations
# Marek Sotak - http://twitter.com/sotak
# My second python script ever ;)
###############################################################################

import scraperwiki
import lxml.html

# starting_url = 'http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/SearchResult.aspx'
# pager http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/SearchResult.aspx?stranka=1

#i = scraperwiki.sqlite.get_var('last_id', 1)
i = 1;
# get the first 500 pages
for i in range(i, i+2):
    # retrieve a page
    # TODO: handle errors
    #starting_url = 'http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/Default.aspx'
    # starting_url = 'http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/SearchResult.aspx?stranka=' + str(i)
    starting_url ="http://aplikace.mvcr.cz/seznam-obcanskych-sdruzeni/Default.aspx?__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=%2FwEPDwULLTIxMTMyNDAyODZkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYFBTJjdGwwMCRjdGwwMCRBcHBsaWNhdGlvbiRCYXNlUGxhY2VIb2xkZXIkQ0JMX1N0YXYkMAUyY3RsMDAkY3RsMDAkQXBwbGljYXRpb24kQmFzZVBsYWNlSG9sZGVyJENCTF9TdGF2JDEFMmN0bDAwJGN0bDAwJEFwcGxpY2F0aW9uJEJhc2VQbGFjZUhvbGRlciRDQkxfU3RhdiQyBTJjdGwwMCRjdGwwMCRBcHBsaWNhdGlvbiRCYXNlUGxhY2VIb2xkZXIkQ0JMX1N0YXYkMwUyY3RsMDAkY3RsMDAkQXBwbGljYXRpb24kQmFzZVBsYWNlSG9sZGVyJENCTF9TdGF2JDNfhXwjJ2xPMtk9kY5c1D%2FfUZzR2g%3D%3D&ctl00%24ctl00%24Application%24BasePlaceHolder%24TB_nazev_Sdruzeni=&ctl00%24ctl00%24Application%24BasePlaceHolder%24Date1=&ctl00%24ctl00%24Application%24BasePlaceHolder%24Date2=&ctl00%24ctl00%24Application%24BasePlaceHolder%24TB_ICO=&ctl00%24ctl00%24Application%24BasePlaceHolder%24TB_Adresa=&ctl00%24ctl00%24Application%24BasePlaceHolder%24BTN_Show_All=Zobrazit+v%C5%A1echny&__EVENTVALIDATION=%2FwEWDALN0f7cCAKX76HUCgLy7eHFAgLy7eXFAgLy7dnFAgLy7d3FAgKOnqa5CQKRnqa5CQKTm4PtBgL8zswyAvqwxtYCAqSf58kItw06oX1W4ZhaWTWRQuaU7zA%2Fia8%3D";
    html = scraperwiki.scrape(starting_url)
    print html
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("#searchResults tr"):
        tds = tr.cssselect("td")
        data = {
          'country' : tds[0].text_content()
        }
        print data
