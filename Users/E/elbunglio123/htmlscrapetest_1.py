

# Blank Python

import scraperwiki
import lxml.html
html = scraperwiki.scrape("https://www.patientopinion.org.uk/opinions/73316") 
root = lxml.html.fromstring(html)
el = root.cssselect("div.story_copy p")[1]
print el.text


