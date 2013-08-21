# Python test code

import scraperwiki
import BeautifulSoup
import urllib2
import string

lastrec = 90100
i = 89999

while i < lastrec:
    try:
        html = scraperwiki.scrape('http://www.expopage.net/portal/stand.do?eboothid=' + str(i))
        soup = BeautifulSoup.BeautifulSoup(html)
        id_expo=i
        i=i+1
        id_str = str(id_expo) 
        print id_str
        html = scraperwiki.scrape('http://www.expopage.net/portal/stand.do?eboothid=' + str(i))
        #print html

        import lxml.html
        root = lxml.html.fromstring(html) # turn our HTML into an lxml object
        tds = root.cssselect('td') # get all the <td> tags
        for td in tds:
            print lxml.html.tostring(td) # the full HTML tag
            print td.text                # just the text inside the HTML tag
        for td in tds:
             record = { "td" : td.text } # column name and value
             scraperwiki.sqlite.save(["td"], record) # save the records one by one

    except:
        i=i+1
        continue
