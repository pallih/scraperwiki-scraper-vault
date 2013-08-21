import scraperwiki
import urlparse
import lxml.html


def scrape_author(author):
    root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    tds = root.cssselect('dt.quote a') # get all the <td> tags
    for td in tds:
    #print lxml.html.tostring(td) # the full HTML tag
        print td.text                # just the text inside the HTML tag

    for td in tds:
         record = { "td" : td.text } # column name and value
         scraperwiki.sqlite.save(["td"], record) # save the records one by one
    

#html = scraperwiki.scrape('http://www.quotationspage.com/quotes/Albert_Einstein/')
html = scraperwiki.scrape('http://www.quotationspage.com/quotes/Mark_Twain/')
scrape_author('foo')


