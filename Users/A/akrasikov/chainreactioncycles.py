import scraperwiki
import lxml.html
import datetime

# Blank Python

ID = "72444"
url = "http://www.chainreactioncycles.com/Models.aspx?ModelID="
html = scraperwiki.scrape(url + ID)
root = lxml.html.fromstring(html)

label = root.cssselect("span[id='ModelsDisplayStyle4_LblTitle']")[0].text
price = root.cssselect("span[id='ModelsDisplayStyle4_LblMinPrice']")[0].text
summary = label + ": " + price

data = {
    'id': ID,
    'link': url,
    'title': "Price for " + label,
    'description': summary,
    'price': price,
    'pubDate': str(datetime.datetime.now())
}

scraperwiki.sqlite.save(unique_keys = ['id'], data = data)