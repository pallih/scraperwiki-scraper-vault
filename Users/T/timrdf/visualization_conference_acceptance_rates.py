import re
import scraperwiki
#html = scraperwiki.scrape('http://eagereyes.org/acceptance-rates')
#print html

# from BeautifulSoup import BeautifulSoup
# soup = BeautifulSoup(html) # turn our HTML into a BeautifulSoup object
#for t in soup.findAll('table'):
#    ths = tr.findAll("thead");
#    if len(ths) == 4:
#        for th in tds:
#            print th

#import lxml.html
#root = lxml.html.fromstring(html)
#for tr in root.cssselect("div[align='left'] tr"):
#    tds = tr.cssselect("td")
#    if len(tds)==12:
#        data = {
#            'country' : tds[0].text_content(),
#            'years_in_school' : int(tds[4].text_content())
#        }
#        print data