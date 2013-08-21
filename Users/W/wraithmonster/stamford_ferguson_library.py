import scraperwiki
import lxml.html
import lxml.etree
import dateutil.parser

URL = 'http://www.eventkeeper.com/code/events.cfm?curOrg=FERGUSON'

TMPLINK = 'http://www.eventkeeper.com/code/events.cfm?curOrg=FERGUSON&curApp=events&curMonth=7&curYear=2013&SelectedDate=7/12/2013#7/12/2013'
TMPLINKSHORTER = 'http://www.eventkeeper.com/code/events.cfm?curOrg=FERGUSON#7/12/2013'

html = scraperwiki.scrape(URL)
parser = lxml.etree.XMLParser(ns_clean=True,recover=True)

tree = lxml.html.fromstring(html)
#tree = lxml.etree.parse(unicode(html, "utf8"))

r = tree.xpath('//table/tbody/tr/td[2]/table/tbody/tr/td/font')

s = tree.xpath('//table')

print r

print s