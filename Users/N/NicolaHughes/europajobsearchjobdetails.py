import scraperwiki
import lxml.html

scraperwiki.sqlite.attach('europajobsearch')

urls = scraperwiki.sqlite.select('URL from `swdata` limit 10')

for url in urls:
    site  = url["URL"]

#site = "http://ec.europa.eu/eures/eures-searchengine/servlet/ShowJvServlet?lg=EN&pesId=62&uniqueJvId=977095N&nnImport=false"

    html = scraperwiki.scrape(site)
    root = lxml.html.fromstring(html)
    print root.text_content()
    tds = root.cssselect('td')
    i = 0
    for td in tds:
        i += 1
        if td.text_content() == "Geographical Information":
            country = tds[i].text_content()
            region =  tds[i+1].text_content()
            print site, country, region
    
        if td.text_content() == "Other Information":
            posts = tds[i].text_content()
            j = 0
            try:
                for j in range(3):
                    j +=1
                    #print tds[i+j].text_content()
                    #print len(tds[i+j].text_content())
                    if len(tds[i+j].text_content()) == 3 or len(tds[i+j].text_content()) == 4:
                        isco = tds[i+j].text_content()
                        print posts, isco
            except Exception as e:
                print "Exception: ", e

import scraperwiki
import lxml.html

scraperwiki.sqlite.attach('europajobsearch')

urls = scraperwiki.sqlite.select('URL from `swdata` limit 10')

for url in urls:
    site  = url["URL"]

#site = "http://ec.europa.eu/eures/eures-searchengine/servlet/ShowJvServlet?lg=EN&pesId=62&uniqueJvId=977095N&nnImport=false"

    html = scraperwiki.scrape(site)
    root = lxml.html.fromstring(html)
    print root.text_content()
    tds = root.cssselect('td')
    i = 0
    for td in tds:
        i += 1
        if td.text_content() == "Geographical Information":
            country = tds[i].text_content()
            region =  tds[i+1].text_content()
            print site, country, region
    
        if td.text_content() == "Other Information":
            posts = tds[i].text_content()
            j = 0
            try:
                for j in range(3):
                    j +=1
                    #print tds[i+j].text_content()
                    #print len(tds[i+j].text_content())
                    if len(tds[i+j].text_content()) == 3 or len(tds[i+j].text_content()) == 4:
                        isco = tds[i+j].text_content()
                        print posts, isco
            except Exception as e:
                print "Exception: ", e

