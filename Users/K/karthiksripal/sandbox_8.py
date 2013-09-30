import scraperwiki
import lxml.html

# Blank Python

for n in range(0,8):
    print n 

html = scraperwiki.scrape('http://news.ycombinator.com/')


print html


root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags
for td in tds:
    print lxml.html.tostring(td) # the full HTML tag
    print td.text                # just the text inside the HTML tag
import scraperwiki
import lxml.html

# Blank Python

for n in range(0,8):
    print n 

html = scraperwiki.scrape('http://news.ycombinator.com/')


print html


root = lxml.html.fromstring(html) # turn our HTML into an lxml object
tds = root.cssselect('td') # get all the <td> tags
for td in tds:
    print lxml.html.tostring(td) # the full HTML tag
    print td.text                # just the text inside the HTML tag
