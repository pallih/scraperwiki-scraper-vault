import scraperwiki
import lxml.etree
import lxml.html
import mechanize
import re
import time

def getCompanies(page = 1):
    print "Grabbing Symbol data from page " + str(page)

    url = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/main-market/main-market.html?page=' + str(page)
    response = browser.open(url)
    root = lxml.html.parse(response).getroot()


    
    rows = root.cssselect(".table_dati tr")
    for tr in rows[1:]:
        link = tr[1][0].attrib.get("href")
        data = {}
        data['symbol'] = tr[0].text
        data['name'] = tr[1][0].text

        key = link.partition('?fourWayKey=')[2]

        info = getCompanyInfo(key)
        data['address'] = info[0]
        data['sector'] = info[1]

        data['fourWayKey'] = key


        scraperwiki.sqlite.save(['symbol'], data, table_name='companies')

def getNews(symbol):
    result = scraperwiki.sqlite.select("fourWayKey FROM companies WHERE symbol='"+symbol+"'")
    print result[0]['fourWayKey']

    url = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/exchange-insight/company-news.html?fourWayKey=' + result[0]['fourWayKey']
    
    response = browser.open(url)
    root = lxml.html.parse(response).getroot()

    newsItems = root.cssselect('#newsArchive div ul li')

    for item in newsItems:
        contents = item.cssselect('div *')
        
        url = contents[0].attrib.get('href')
        id = re.search('\?announcementId=([0-9]*)', url).group(1)

        data = {}
        data['id'] = id
        data['symbol'] = symbol
        data['time'] = getAnnouncementDate(id)
        data['title'] = contents[0].text.strip()

        scraperwiki.sqlite.save(['id'], data, table_name='announcements')

def getCompanyInfo(fourWayKey):
    url = 'http://www.londonstockexchange.com/exchange/prices-and-markets/stocks/summary/company-summary.html?fourWayKey=' + fourWayKey
    response = browser.open(url)
    
    root = lxml.html.parse(response).getroot()

    address = root.xpath("//table[@summary='Company Information']/tbody/tr[position()=1]/td[position()=2]")[0].text
    sector = root.xpath("//table[@summary='Trading Information']/tbody/tr[position()=2]/td[position()=2]")[0].text

    return address, sector
    

def getAnnouncementDate(announcementId):
    url = 'http://www.londonstockexchange.com/exchange/news/market-news/market-news-detail.html?announcementId=' + str(announcementId)
    response = browser.open(url)
    root = lxml.html.parse(response).getroot()

    r = root.xpath("//tr[td[.='Released']]/td[position()=2]")
    return time.strftime("%Y-%m-%d %H:%S", time.strptime(r[0].text, "%H:%S %d-%b-%Y"))


fields = ['symbol VARCHAR UNIQUE PRIMARY KEY', 'fourWayKey VARCHAR' ]
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS companies (%s)" % ", ".join(fields))
fields = ['id INTEGER PRIMARY KEY', 'symbol', 'date DATETIME', 'title VARCHAR']
scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS announcements (%s)" % ", ".join(fields))

browser = mechanize.Browser()
browser.addheaders = [ ['User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'] ]

for i in range(25, 999):
    getCompanies(i)
#getNews("ADM")