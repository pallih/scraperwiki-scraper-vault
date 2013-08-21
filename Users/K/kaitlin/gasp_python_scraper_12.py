import scraperwiki
import urllib2 as ulib
from lxml import html
from dateutil.parser import parse as dateparse

gasp_helper = scraperwiki.utils.swimport("gasp_helper")


# This is a Python template for a Sunlight Labs Great American Scraper Project 
# http://services.sunlightlabs.com/gasp/legislators/


# Step 1) PLACE YOUR CONFIG LINE HERE

gasp = gasp_helper.GaspHelper("6a95690d3cd44fc2b7fd1d37a63e605d", "H000874")


# Step 2) Write Your Scraper Here
#         (refer to https://scraperwiki.com/scrapers/gasp_helper for documentation)


headers = {
                    "Host":"www.democraticwhip.gov",
                    "User-Agent":"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.23) Gecko/20110921 Ubuntu/10.04 (lucid) Firefox/3.6.23",
                    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language":"en-us,en;q=0.5",
                    "Accept-Encoding":"identity",
                    "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                    "Keep-Alive": '115',
                    "Connection":"keep-alive",
                    "Cookie": "SESSe44492e3eff92ed36c02b54ede745fd0=f8u762lhlmo02lf6s9f1q58s83; has_js=1",
                    "If-Modified-Since":"Mon, 05 Mar 2012 21:05:37 GMT",
                    "If-None-Match": "80b1e5f8cd8bc5180b65f43da511070c",
                    "Cache-Control":"max-age=0",
                    "Content-Type":"text/html; charset=utf-8"
        }
request = ulib.Request("http://www.democraticwhip.gov/newsroom/press-releases", headers=headers)
data = ulib.urlopen(request).read()

page = html.fromstring(data)
page.make_links_absolute("www.democraticwhip.gov")

linklist = page.find_class('views-row')

for item in linklist:
    link = "http://www.democraticwhip.gov" + item.find('.//a').get('href')
    title = item.find('.//a').text_content()
    date = item.find_class('date-display-single')[0].text_content()

    #get content of link
    req = ulib.Request(link, headers=headers)
    d = ulib.urlopen(req).read()
    p = html.fromstring(d)
    p.make_links_absolute("www.democraticwhip.gov")
    content = p.get_element_by_id("content-area").find_class('content')[0].text_content() #.find_class("content")[0].text_content()
    
    print link
    print date
    print title
    print content
    extra = {'url': link}
    gasp.add_press_release(title, date, content, extra=extra)


# Step 3) Run Your Scraper
#         call gasp.finish() to let our server know your scraper succeeded
gasp.finish()