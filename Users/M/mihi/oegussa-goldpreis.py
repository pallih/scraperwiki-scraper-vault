import scraperwiki
import datetime
import lxml.html

# Blank Python

url="http://www.oegussa.at/neu/kurse/edelmat.htm"

h=scraperwiki.scrape(url)
root=lxml.html.fromstring(h)

commodities=root.cssselect("#BARVERKAUF tr")[1:]

date=datetime.date.today()

for c in commodities:
    [name,price,null]=[i.text_content() for i in c.cssselect("td")]
    price=price.strip().replace(".","").replace(",",".")
    data={"name":name,"price":price, "date":date, "unique":"%s-%s"%(date,name)}
    scraperwiki.sqlite.save(unique_keys=["unique"],data=data)
    

