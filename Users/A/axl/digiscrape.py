import scraperwiki

html = scraperwiki.scrape('http://www.akseldybdal.com')
#print "Click on the ...more link to see the whole page"
#print html

import lxml.html
root = lxml.html.fromstring(html)    # turn our HTML into an lxml object                 

posts = root.cssselect("a[class='post']") # Get all "post"
for post in posts:
    print lxml.html.tostring(post)     
    print post.text 

paragraphs = root.cssselect("p") # Get all "paragraphs"
for paragraph in paragraphs:
    print lxml.html.tostring(paragraph)     
    print paragraph.text 

slides = root.cssselect("ul[class='slides']") # Get all "slides"
for slide in slides:
    print lxml.html.tostring(slide)     
    print slide.text import scraperwiki

html = scraperwiki.scrape('http://www.akseldybdal.com')
#print "Click on the ...more link to see the whole page"
#print html

import lxml.html
root = lxml.html.fromstring(html)    # turn our HTML into an lxml object                 

posts = root.cssselect("a[class='post']") # Get all "post"
for post in posts:
    print lxml.html.tostring(post)     
    print post.text 

paragraphs = root.cssselect("p") # Get all "paragraphs"
for paragraph in paragraphs:
    print lxml.html.tostring(paragraph)     
    print paragraph.text 

slides = root.cssselect("ul[class='slides']") # Get all "slides"
for slide in slides:
    print lxml.html.tostring(slide)     
    print slide.text 