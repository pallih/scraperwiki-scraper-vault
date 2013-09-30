import scraperwiki
import lxml.html
import mechanize
html = scraperwiki.scrape("http://www.wipo.int/amc/en/domains/search/text.jsp?case=D2013-00019")
root = lxml.html.fromstring(html)

br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (Firefox/3.0.1')]


for el in root.cssselect("div.featured a"): print el
import scraperwiki
import lxml.html
import mechanize
html = scraperwiki.scrape("http://www.wipo.int/amc/en/domains/search/text.jsp?case=D2013-00019")
root = lxml.html.fromstring(html)

br = mechanize.Browser()
# Set the user-agent as Mozilla - if the page knows we're Mechanize, it won't return all fields
br.addheaders = [('User-agent', 'Mozilla/5.0 (Firefox/3.0.1')]


for el in root.cssselect("div.featured a"): print el
