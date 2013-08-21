import scraperwiki
import requests
import lxml.html

r = requests.get("https://www.airbnb.co.uk/s/Stockholm--Sweden?page=1", verify=False)
dom = lxml.html.fromstring(r.text)
targetList = dom.cssselect('.search_result a.name')
ads = []

for result in targetList:
    ad = {
        "title": result.text_content(),
        "url": result.get("href")
    }
    ads.append(ad)

for theAd in ads:
    r2 = requests.get("https://airbnb.co.uk" + theAd["url"], verify=False)
    dom2 = lxml.html.fromstring(r2.text)

    value = dom2.cssselect("#price_amount")[0].text_content()
    key = "price"
    theAd[key] = value

scraperwiki.sqlite.save(["url"], ads)
