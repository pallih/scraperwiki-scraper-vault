MAINTENANCE = False

import scraperwiki
import lxml.html
from datetime import datetime
from datetime import timedelta


def clean_trash():
    print "Cleaning trash"
    sql = "delete from swdata where date like '%%.%%.2013'"
    res = scraperwiki.sqlite.execute(sql)
    for line in res['data']:
        print line

def parse_sold_text(text):
    day = timedelta(days=1)
    if u"T\xe4n\xe4\xe4n" or u"T\xc3\xa4n\xc3\xa4\xc3\xa4n" in text:
        return None
    elif u"Eilen" in text:
        sold_date = datetime.now() - day
        return sold_date.date()
    else:
        sold_date = datetime.now() - day * int(text.split()[0])
        return sold_date.date()

def main():
    phones = []

    querypage_url = "http://www.verkkokauppa.com/fi/s?s=1&q=&submit=Hae&category=22-658-4814&brand=Nokia"
    querypage_html = scraperwiki.scrape(querypage_url)
    querypage_root = lxml.html.fromstring(querypage_html)

    for el in querypage_root.cssselect("div.productRow"):
        stock = el.cssselect("div.stock")[0].text
        if "ennakkotilaa" not in stock:
            product_url = el.cssselect("a.productInfo")[0].attrib["href"]
            phones.append({'url':product_url})

    for phone in phones:
        url_parts = phone["url"].split("/")
        phone_model = url_parts[-1]
        product_code = url_parts[-3] + url_parts[-2]
        phone_html = scraperwiki.scrape(phone["url"])
        phone_root = lxml.html.fromstring(phone_html)
        for el in phone_root.cssselect("div#latestSoldList li"):
            if el.text:
                try:
                    sold_date = datetime.strptime(el.text[3:], "%d.%m.%Y %H:%M")
                except:
                    sold_date = parse_sold_text(el.text)
                if sold_date:
                    sold_pieces = el.cssselect("span")[0].text
                    sold_pieces = [int(s) for s in sold_pieces.split() if s.isdigit()][0] # because "8 kpl", "yli 20 kpl" cases
                    scraperwiki.sqlite.save(unique_keys=['pcode','date'], data=({"pcode":product_code,"model":phone_model,"date":sold_date,"pieces":sold_pieces}))

if MAINTENANCE:
    clean_trash()
else:
    main()
