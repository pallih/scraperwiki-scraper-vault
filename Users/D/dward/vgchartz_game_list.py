import scraperwiki
import lxml.html  

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS gamedata ('Title' string, 'Platform' string, 'Year' string, 'Genre' string, 'Publisher' string, 'US Sales' real, 'Europe Sales' real, 'Japan Sales' real, 'Others Sales' real, 'Global Sales' real, PRIMARY KEY('Title', 'Platform'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO gamedata ('Title', 'Platform', 'Year', 'Genre', 'Publisher', 'US Sales', 'Europe Sales', 'Japan Sales', 'Others Sales', 'Global Sales') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data['Title'], data['Platform'], data['Year'], data['Genre'], data['Publisher'], data['US_Sales'], data['Europe_Sales'], data['Japan_Sales'], data['Others_Sales'], data['Global_Sales']))
    scraperwiki.sqlite.commit()

def scrapeAndSave(url):
    html = scraperwiki.scrape(url)

    root = lxml.html.fromstring(html)
    for tr in root.cssselect("div#chart_body .chart tr"):
        tds = tr.cssselect("td")
        if len(tds) == 11:
            data = {
                'Title' : tds[1].text_content(),
                'Platform' : tds[2].text_content(),
                'Year' : tds[3].text_content(),
                'Genre' : tds[4].text_content(),
                'Publisher' : tds[5].text_content(),
                'US_Sales' : float(tds[6].text_content()),
                'Europe_Sales' : float(tds[7].text_content()),
                'Japan_Sales' : float(tds[8].text_content()),
                'Others_Sales' : float(tds[9].text_content()),
                'Global_Sales' : float(tds[10].text_content())
            }
            saveToStore(data)    

# Scraping PC list
scrapeAndSave("http://www.vgchartz.com/gamedb/?name=&publisher=&platform=PC&genre=&minSales=0&results=8000")

# Scraping Xbox 360 list
scrapeAndSave("http://www.vgchartz.com/gamedb/?name=&publisher=&platform=X360&genre=&minSales=0&results=4000")

# Scraping PS3 list
scrapeAndSave("http://www.vgchartz.com/gamedb/?name=&publisher=&platform=PS3&genre=&minSales=0&results=4000")

# Scraping Wii list
scrapeAndSave("http://www.vgchartz.com/gamedb/?name=&publisher=&platform=Wii&genre=&minSales=0&results=4000")
