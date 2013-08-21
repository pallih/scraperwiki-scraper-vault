import mechanize
import lxml.html
import scraperwiki

# Blank Python
br = mechanize.Browser()
r = br.open('http://www.yelp.com/sydney')
html = r.read()
#.encode('utf-8').strip()
#html=scraperwiki.scrape("http://www.airbagan.com/winter-flightschedule-yangon.htm")
print html


