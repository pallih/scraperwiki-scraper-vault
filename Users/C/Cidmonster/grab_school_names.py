import scraperwiki
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import lxml.html
from lxml.cssselect import CSSSelector

def Main():
    school = ''
    schoollist = []
    html = scraperwiki.scrape('http://www.naicu.edu/member_center/members.asp')
    root = lxml.html.fromstring(html)
    sel = CSSSelector('a.searchLink')    # type of tags to look at
    for a in sel(root):
        if a.text:
            print a.text
            record = {}
            record['school'] = a.text
            scraperwiki.sqlite.save(['school'], record)

Main()



