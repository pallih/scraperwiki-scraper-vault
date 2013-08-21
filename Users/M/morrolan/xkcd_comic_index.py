#!/usr/bin/python

import scraperwiki     # Scraperwiki is web-based - import only currently works through the Scraperwiki web interface.
import lxml.html       # lxml is used to parse the website that is scraped.


html = scraperwiki.scrape("http://xkcd.com/archive/")     # set a string into which we will load/scrape the ENTIRE HTML for the target page!
root = lxml.html.fromstring(html)                         # load the HTML into an object from lxml so we can parse through it


main_url = 'http://xkcd.com'                              # set the main website URL - individual comic URLs willo be stitched onto the end of this

try:                                                      # try/catch block in case the table doesn't exist - if it doesn't, a try/catch will cope with the error
    scraperwiki.sqlite.execute("drop table swdata")       # good practice to drop the entire table and do a whole new scrape each time rather than amending data
except:
    pass

print html  # clearly works here but the for loop below iswn't being reached/evaluated.

for el in root.cssselect("div.box a"):        # el is element in the CSS Selector/lxml - every time it finds an <a tag in the 's' div

#for el in root.etree("div#middleContainer"):

    #print el.attrib

    page_url = el.attrib['href']                          # nick the individual comic URL
    date_published = el.get('title')                      # grab the published date - what a bitch this was!
    comic_url = main_url + page_url                       # stitch together the main page url above and the individual URL scraped above
    comic_title = el.text                                 # here we simply need to grab the text of the <a tag
    comic_no = page_url.replace('/','')                   # much neater to do a proper string replace

    
    if comic_title == 'Archive':                          # We want to NOT save unwanted <a tags within the 's' div
        print 'Skipping: ' + comic_title
        continue

    if comic_title == 'News/Blag':                        # as above
        print 'Skipping: ' + comic_title
        continue

    if comic_title == 'Store':                            # as above
        print 'Skipping: ' + comic_title
        continue

    if comic_title == 'About':                            # as above
        print 'Skipping: ' + comic_title
        continue

    if comic_title == 'Forums':                           # as above
        print 'Skipping: ' + comic_title
        continue

    if page_url == '/':                                   # here we detect the first comic, so now we need to start processing
        print 'Root Detected - now processing URLs'
        comic_title = 'Current Comic'

    if page_url == '/rss.xml':                            # this is the first URL immediately after the comics, so now we stop (break)
        print 'End Detected - will now stop parsing URLs'
        break

    


    xkcd_data = {                                              # here we save the collected data into a dict
      'comic_url' : comic_url,
      'comic_title' : comic_title,
      'date_published' : date_published,
      'comic_no' : comic_no
    }
    print xkcd_data


    scraperwiki.sqlite.save(unique_keys=['comic_url'], data=xkcd_data)     # save the data to the SQLite table - primary key being the URL number, and then adding the data





