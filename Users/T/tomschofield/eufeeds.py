import scraperwiki
import lxml.html
import string


#get html object
url = "http://eufeeds.eu"
html = scraperwiki.scrape(url)

root = lxml.html.fromstring(html)
#to keep track of where we are
myVar=0
tableCount=0
#python for loops need a colon and then indentation to work! 
#counter for each individual domain on each level - reset at each level
domainID=0

#GET LINKS FROM FIRST PAGE
for el in lxml.html.iterlinks(html):
    print el[0]