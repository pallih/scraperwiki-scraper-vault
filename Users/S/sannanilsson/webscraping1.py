import scraperwiki
import requests 
import lxml.html

r = requests.get("http://airbnb.herokuapp.com/")
dom = lxml.html.fromstring(r.text) 

targetList = dom.cssselect(".search_result a.name")

ads = []

for result in targetList: 
    ad = {
        "title": result.text_content(), 
        "url": result.get("href")
    }
    ads.append(ad)

for theAd in ads: 
    r2 = requests.get(theAd["url"], verify=False)
    dom2= lxml.html.fromstring(r2.text)
    
    price = dom2.cssselect("#price_amount")
    print price