import scraperwiki
import lxml.html
#this library is used to create a list of letters A-Z with the method ascii_lowercase
import string

# http://www.oiahe.org.uk/decisions-and-publications/annual-letters.aspx

def scrapepdf(fulllink):
    html = scraperwiki.scrape(fulllink)
    print html
    root = lxml.html.fromstring(html)

def scrapelinks(starturl):
    html = scraperwiki.scrape(starturl)
    root = lxml.html.fromstring(html)
    print root
    tds = root.cssselect('table td p strong a')
    for td in tds:
        print td.attrib.get('href')
        fulllink = 'http://www.oiahe.org.uk'+td.attrib.get('href')
        print "scraping PDF:", fulllink
        scrapepdf(fulllink)
        

#NONE OF THIS IS NEEDED BECAUSE ONE PAGE HAS ALL LINKS ANYWAY
#baseurl = 'http://www.oiahe.org.uk/decisions-and-publications/'
#loop through letters A-Z and add to end, e.g.
#http://www.oiahe.org.uk/decisions-and-publications/annual-letters/alphabetically.aspx#B
#for char in string.ascii_lowercase:
 #   print char
  #  starturl = baseurl+'annual-letters/alphabetically.aspx#'+char
   # print starturl

scrapelinks('http://www.oiahe.org.uk/decisions-and-publications/annual-letters/alphabetically.aspx#A')

