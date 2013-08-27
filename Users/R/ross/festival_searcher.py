# Testing the page as it doesn't work (css for body) with nokogiri.
import scraperwiki
from lxml.html import fromstring

print "Scraping FestivalSearcher.com..."
html = scraperwiki.scrape("http://www.festivalsearcher.com/festivallists.aspx?region=uk")
page = fromstring(html)
print page.cssselect('body')# Testing the page as it doesn't work (css for body) with nokogiri.
import scraperwiki
from lxml.html import fromstring

print "Scraping FestivalSearcher.com..."
html = scraperwiki.scrape("http://www.festivalsearcher.com/festivallists.aspx?region=uk")
page = fromstring(html)
print page.cssselect('body')# Testing the page as it doesn't work (css for body) with nokogiri.
import scraperwiki
from lxml.html import fromstring

print "Scraping FestivalSearcher.com..."
html = scraperwiki.scrape("http://www.festivalsearcher.com/festivallists.aspx?region=uk")
page = fromstring(html)
print page.cssselect('body')