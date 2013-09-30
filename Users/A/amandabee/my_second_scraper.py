import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.nyc.gov/html/nypd/html/traffic_reports/traffic_summons_reports.shtml")
page = lxml.html.fromstring(html)

# Select the second <blockquote> element on the page (the first would be [0]).
bq2 = page.cssselect("blockquote")[1] 

for para in bq2.cssselect("p.row"): 
    # Select the first <a> element in the paragraph as the title.

    URL = para.cssselect("a")[0].attrib['href']
    listing = lxml.html.fromstring(scraperwiki.scrape(URL))
    
#    for el in listing.cssselect("div#userbody"): 
    for el in listing.cssselect("table"):
        if (el.attrib['summary'] == "craigslist hosted images"):
            if el.cssselect('img'):    
                imgs = el.cssselect('img')
                image = imgs[0].attrib['src']
            else: 
                image = ''
#   print el.tag 
#   for el2 in el: 
#       print "--", el2.tag, el2.attrib
    
    data = {
        'image' : image,
        'title' : para.cssselect("a")[0].text_content(),
        'URL' : para.cssselect("a")[0].attrib['href'],
        'nabe' : para.cssselect("font")[0].text_content(),
        'category' : para.cssselect("a")[1].text_content(),
        'price' : para.cssselect("a")[0].tail.strip()
    }

    print data
    scraperwiki.sqlite.save(unique_keys=['URL'], data=data)


# Get LXML documentation at: http://lxml.de/lxmlhtml.html

# Also https://scraperwiki.com/docs/python/python_css_guide/

# And http://blog.ouseful.info/2011/11/13/a-quick-lookup-service-for-uk-university-bursary-scholarship-pages/


import scraperwiki
import lxml.html

html = scraperwiki.scrape("http://www.nyc.gov/html/nypd/html/traffic_reports/traffic_summons_reports.shtml")
page = lxml.html.fromstring(html)

# Select the second <blockquote> element on the page (the first would be [0]).
bq2 = page.cssselect("blockquote")[1] 

for para in bq2.cssselect("p.row"): 
    # Select the first <a> element in the paragraph as the title.

    URL = para.cssselect("a")[0].attrib['href']
    listing = lxml.html.fromstring(scraperwiki.scrape(URL))
    
#    for el in listing.cssselect("div#userbody"): 
    for el in listing.cssselect("table"):
        if (el.attrib['summary'] == "craigslist hosted images"):
            if el.cssselect('img'):    
                imgs = el.cssselect('img')
                image = imgs[0].attrib['src']
            else: 
                image = ''
#   print el.tag 
#   for el2 in el: 
#       print "--", el2.tag, el2.attrib
    
    data = {
        'image' : image,
        'title' : para.cssselect("a")[0].text_content(),
        'URL' : para.cssselect("a")[0].attrib['href'],
        'nabe' : para.cssselect("font")[0].text_content(),
        'category' : para.cssselect("a")[1].text_content(),
        'price' : para.cssselect("a")[0].tail.strip()
    }

    print data
    scraperwiki.sqlite.save(unique_keys=['URL'], data=data)


# Get LXML documentation at: http://lxml.de/lxmlhtml.html

# Also https://scraperwiki.com/docs/python/python_css_guide/

# And http://blog.ouseful.info/2011/11/13/a-quick-lookup-service-for-uk-university-bursary-scholarship-pages/


