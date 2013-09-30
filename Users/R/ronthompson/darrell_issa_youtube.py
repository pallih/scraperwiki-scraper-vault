# Darrell Issa YouTube

import scraperwiki
html = scraperwiki.scrape("http://www.youtube.com/user/RepDarrellIssa/about")
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
lis = root.cssselect('li class="about-stats"') # get all the <td> tags
for li in lis:
    print lxml.html.tostring(li) # the full HTML tag
    print li.text                # just the text inside the HTML tag

# Darrell Issa YouTube

import scraperwiki
html = scraperwiki.scrape("http://www.youtube.com/user/RepDarrellIssa/about")
print html

import lxml.html
root = lxml.html.fromstring(html) # turn our HTML into an lxml object
lis = root.cssselect('li class="about-stats"') # get all the <td> tags
for li in lis:
    print lxml.html.tostring(li) # the full HTML tag
    print li.text                # just the text inside the HTML tag

