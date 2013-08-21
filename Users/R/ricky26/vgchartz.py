import scraperwiki
import lxml.html  
import datetime

sw = scraperwiki
db = sw.sqlite
date = datetime.date

rooturl = "http://www.vgchartz.com"

"""for tr in root.cssselect('#innerContent tr'):
    img = tr.cssselect('img')
    if len(img):
        imgURL = img[0].attrib['src']
        
        try:
            name = tr.cssselect('a')[-1].text_content()
            amount = int(tr.cssselect('td')[-1].text_content().replace(",",""))
            data = {'imgURL': imgURL, 'name': name, 'amount':amount}
            db.save(unique_keys=['name'], data=data)
            print data
        except:
            pass"""

earliestDate = date(1900, 1, 1)
stopDate = date(2004, 11, 1)

def scrapeConsolesWeek(starting):
    delta = starting-earliestDate
    days = (delta.days/7)*7 + 1
    url = "%s/weekly/%d/Global/" % (rooturl, days)
    html = sw.scrape(url)
    root = lxml.html.fromstring(html)
    tb = root.cssselect("#rightbar table")[0]

    print days

    data = {'date':starting}
    
    for tr in tb.cssselect("tr")[1:-1]:
        console = str(tr[0].text_content())
        amount = int(tr[-1].text_content().replace(",",""))
        data[console] = amount
        
    db.save(unique_keys=['date'], data=data)

week = datetime.timedelta(7)
b = date.today() - week
while b > stopDate:
    scrapeConsolesWeek(b)
    b -= week*4