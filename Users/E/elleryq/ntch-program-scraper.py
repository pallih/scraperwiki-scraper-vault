# For http://www.ntch.edu.tw/program/showByCategory?categoryName=program_family&lang=zh
import scraperwiki
import simplejson
import lxml.html
import sys
from urlparse import parse_qs
from urllib import urlencode
import traceback

base_url = 'http://www.ntch.edu.tw/program/showByCategory?categoryName=program_family&lang=zh'

def parse_from_html(html):
    root = lxml.html.fromstring(html)
    for tag in root.cssselect("div.thisMonthProgram.row"):
        children = tag.getchildren()
        for child in children:
            print(child.text_content().decode('big5'))
        #print(tag.getnext().getnext().text())

#
# Main
#
def main():
    try:
        html = scraperwiki.scrape( base_url )
        parse_from_html( html )
    except Exception, e:
        print( "Got exception:" )
        print( e )
        print( traceback.format_exc() )

main()

