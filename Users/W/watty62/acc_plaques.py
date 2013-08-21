import scraperwiki

# Blank Python

import lxml.html
#html = scraperwiki.scrape("http://www.aberdeencity.gov.uk/xcp_PlaqueList.asp")
#root = lxml.html.fromstring(html)


def scrape_sub(url_in):
    #print url_in
    sub_html = scraperwiki.scrape(url_in)
    print sub_html
    sub_root = lxml.html.fromstring(sub_html)

    #for el in root.cssselect("div#content-app-body"):
    #    print el
    #root = lxml.html.fromstring(html) # turn our HTML into an lxml object
    #tds = root.cssselect('td') # get all the <td> tags
    #for td in tds:
    #    print lxml.html.tostring(td) # the full HTML tag
    #    print td.text                # just the text inside the HTML tag

    title = sub_root.cssselect('h3')
    
    for t in title:
        print t.text

#for el in root.cssselect("div#content-app-body a"):
#     scrape_sub("http://www.aberdeencity.gov.uk/" + el.attrib['href'])
scrape_sub("http://www.aberdeencity.gov.uk/xcp_PlaqueResult.asp?rec=1")



