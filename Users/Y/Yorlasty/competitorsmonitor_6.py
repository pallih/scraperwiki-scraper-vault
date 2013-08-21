import scraperwiki
import scraperwiki           
import lxml.html 
import uuid
import datetime

# Blank Python

ASINS = ["B006K3KTPC","B0051UGYXG","B003U9V7SC","B004E9QSO0","B004R9OSS0","B0042KXAQA","B005G0YMLC","B006Y8GX4E","B003Y3B1NU","B003W57Z6W","B007P3DHVY","B005KIQ1C8","B004OT6NWW","B002Q4U724","B0027P88RS","B002Y5XNBM","B003VIW43O","B00074ETBK","B005OR0OBY","B000UQ47JO","B0085KLVKK","B008H2QENK","B006YBKWQG","B002MRS5OW","B006JX508E","B003894KGA","B007IZGAAY","B0085K6FOW","B002OOWHM4","B0000AKGX3","B003AM7MYM","B005LAL1PW","B003XII6ZC","B000T76UOE","B0006TU75I","B004W2UMDW","B001NQHN7S","B002QQ7JLY","B005JBQC84","B008HB4FFK","B004GWXLI6","B0038JDUG6","B001U0O190","B003PTIUD2","B000JM2FSE","B0041M5238","B00187HGOW","B0031J8Q4E"]
summary = ""

for asin in ASINS:
    url = "http://www.amazon.co.uk/dp/"+asin
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    summary += asin + " "
    for price in root.cssselect("span[id='actualPriceValue'] b"):
        summary += price .text +"<br>"
        break

now = datetime.datetime.now()
data = {
    'pubDate': str(now) ,
    'link': "http://www.amazon.co.uk/"+"&uuid="+str(uuid.uuid1()),
    'description': summary,
}
scraperwiki.sqlite.save(unique_keys=['link'],data=data)
    

