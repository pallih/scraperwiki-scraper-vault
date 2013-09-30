# import scraperwiki
# emaillibrary = scraperwiki.utils.swimport("general-emails-on-scrapers")
# subjectline, headerlines, bodylines, footerlines = emaillibrary.EmailMessageParts()
# if bodylines:
#   print "\n".join([subjectline] + headerlines + bodylines + footerlines)

import scraperwiki
import lxml.html 
import uuid
import datetime

ASINS = ["B005QJ7OR2","B0078Y0BAK"]
summary = ""

for asin in ASINS:
    url = "http://www.amazon.com/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for title in root.cssselect("span[id='btAsinTitle']"):  
        summary += title.text +":  "
        break
    for price in root.cssselect("span[id='actualPriceValue'] b"):
        summary += price .text +"<br>"
        break
    summary += url + "<br>"

now = datetime.datetime.now()
data = {
    'link': "http://www.amazon.com/"+"&uuid="+str(uuid.uuid1()),
    'title': "Price Monitoring " + str(now),
    'description': summary,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)

