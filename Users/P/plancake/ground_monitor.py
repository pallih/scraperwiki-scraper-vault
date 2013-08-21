import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python


summary = ""

url = "https://www.norwestsoccer.net/"
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
for title in root.cssselect("div#rt-sidebar-a div.box2 h2"):  
    print title.text
    summary += title.text
    break
    

now = datetime.datetime.now()
data = {
    'link': "https://www.norwestsoccer.net/",
    'title': "Ground Monitoring " + str(now),
    'description': summary,
    'pubDate': str(now) ,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)