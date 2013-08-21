import scraperwiki
import mechanize # added by Usha
import re # added by Usha
import lxml.html
url="http://en.wikipedia.org/wiki/List_of_Monuments_of_National_Importance_in_Delhi"
#url="http://www.indiapost.gov.in/"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
print root
              
