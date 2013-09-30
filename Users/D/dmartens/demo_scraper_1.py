import scraperwiki

# Blank Python



import scraperwiki
import lxml.html

print "This is Dave's first ScraperWiki program."

print "Setting page to be scraped."

# html = scraperwiki.scrape("http://en.wikipedia.org/wiki/Wikipedia:WikiProject_Trains/ICC_valuations/Chicago,_Milwaukee_and_St._Paul_Railway")
html = scraperwiki.scrape("http://en.wikipedia.org")

print "Downloaded page to be scraped."

root = lxml.html.fromstring(html)

for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print dataimport scraperwiki

# Blank Python



import scraperwiki
import lxml.html

print "This is Dave's first ScraperWiki program."

print "Setting page to be scraped."

# html = scraperwiki.scrape("http://en.wikipedia.org/wiki/Wikipedia:WikiProject_Trains/ICC_valuations/Chicago,_Milwaukee_and_St._Paul_Railway")
html = scraperwiki.scrape("http://en.wikipedia.org")

print "Downloaded page to be scraped."

root = lxml.html.fromstring(html)

for tr in root.cssselect("div[align='left'] tr"):
    tds = tr.cssselect("td")
    if len(tds)==12:
        data = {
            'country' : tds[0].text_content(),
            'years_in_school' : int(tds[4].text_content())
        }
        print data