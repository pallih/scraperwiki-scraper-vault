import scraperwiki
import mechanize
import cookielib
import urllib2
import BeautifulSoup
from BeautifulSoup import SoupStrainer
print "ok imports"

page = open(r'///Users/maggielee/Documents/pythons/MeetingNotices.webarchive')
print page.read()

soup = BeautifulSoup(page)
#print (soup.prettify())

only_a_tags = SoupStrainer("a")


print (BeautifulSoup(page, "html.parser", parse_only=only_a_tags).prettify())
import scraperwiki
import mechanize
import cookielib
import urllib2
import BeautifulSoup
from BeautifulSoup import SoupStrainer
print "ok imports"

page = open(r'///Users/maggielee/Documents/pythons/MeetingNotices.webarchive')
print page.read()

soup = BeautifulSoup(page)
#print (soup.prettify())

only_a_tags = SoupStrainer("a")


print (BeautifulSoup(page, "html.parser", parse_only=only_a_tags).prettify())
