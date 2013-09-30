import scraperwiki
import requests
import lxml.html

r = requests.get("http://airbnb.co.uk/s/Stockholm--Sweden?page=1",verify=False)
dom = lxml.html.fromstring(r.text)

targetList = dom.cssselect('search_result a.name')

ads = []

for result in targetList:
    ad = {
        "title" : result.text_content(),
        "url" : result.get("href")
        }

for theAd in ads:
    r2 = requests.get(theAd["http://airbnb.co.uk"] + theAd["url"], verify=False)
    dom2 = lxml.html.fromstring(r2.text)
    dom2.cssselect("#price_amount").text_content()
    value = dom2.cssselect("#price_amount")[0].text_content()

key = "value"
print value

import scraperwiki
import requests
import lxml.html

r = requests.get("http://airbnb.co.uk/s/Stockholm--Sweden?page=1",verify=False)
dom = lxml.html.fromstring(r.text)

targetList = dom.cssselect('search_result a.name')

ads = []

for result in targetList:
    ad = {
        "title" : result.text_content(),
        "url" : result.get("href")
        }

for theAd in ads:
    r2 = requests.get(theAd["http://airbnb.co.uk"] + theAd["url"], verify=False)
    dom2 = lxml.html.fromstring(r2.text)
    dom2.cssselect("#price_amount").text_content()
    value = dom2.cssselect("#price_amount")[0].text_content()

key = "value"
print value

