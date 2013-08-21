import scraperwiki
import lxml.html
import datetime

keywords = ['Retina', '512GB Flash']
url = "http://store.apple.com/us/browse/home/specialdeals/mac/macbook_pro/13"

scraperwiki.sqlite.execute('delete from swdata')
html = scraperwiki.scrape(url)
root = lxml.html.fromstring(html)
for tr in root.cssselect("tr.product"):
    for td in tr.cssselect("td.specs"):
        text = td.text_content().strip()

        if all(word in text for word in keywords):
            data = {
                'title': td.cssselect("h3 a")[0].text_content().strip() + " " + tr.cssselect("p.price")[0].text_content().strip(),
                'link': url,
                'description': text,
                'guid': td.cssselect("h3 a")[0].attrib['onclick'].split('=')[1][1:-2],
                'date': str(datetime.datetime.now())
            }
            scraperwiki.sqlite.save(unique_keys=['guid'], data=data)