import scraperwiki
import lxml.html
# Blank Python

print 'hello world'

#this is a comment - its just a not for you or others to read

html = scraperwiki.scrape('http://www.corriere.it/')

print html

#with scraperwiki we can easily find all the links on the page! great!
for aLink in lxml.html.iterlinks(html):
    print aLink[2]