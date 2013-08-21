import scraperwiki
import urllib2
import string

try:
    scraperwiki.sqlite.execute("""
        create table magic
        (
        id INTEGER PRIMARY KEY AUTOINCREMENT
        )
    """)
except:
    print "Table probably already exists."

baseurl = ("http://www.aph.gov.au/Senators_and_Members/Parliamentarian_Search_Results?page=%s&q=&mem=1&sen=1&par=-1&gen=0&ps=100&st=1" % hahaha)

def oneborn():
    html = scraperwiki.scrape(baseurl)

print baseurl

