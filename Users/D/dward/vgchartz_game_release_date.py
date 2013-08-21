import scraperwiki
import lxml.html  

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS game_release_date ('Title' string, 'Publisher' string, 'Platform' string, 'Genre' string, 'Region' string, 'Release_Date' string, PRIMARY KEY('Title', 'Region', 'Platform'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO game_release_date ('Title', 'Publisher', 'Platform', 'Genre', 'Region', 'Release_Date') VALUES (?, ?, ?, ?, ?, ?)", (data['Title'], data['Publisher'], data['Platform'], data['Genre'], data['Region'], data['Release_Date']))
    scraperwiki.sqlite.commit()

def scrapeAndSave(url):
    html = scraperwiki.scrape(url)

    root = lxml.html.fromstring(html)
    for tr in root.cssselect("div#chart_body .chart tr"):
        tds = tr.cssselect("td")
        if len(tds) == 11:
            a = tds[1].cssselect("a")[0]
            game_url = a.attrib["href"]
            game_html = scraperwiki.scrape(game_url)
            game_root = lxml.html.fromstring(game_html)
            title = game_root.cssselect("h1")[0].text_content()
            platform = game_root.cssselect("table#game_infobox tr")[1].cssselect("td")[0].cssselect("a")[0].text_content()
            genre = game_root.cssselect("table#game_infobox tr")[2].cssselect("td")[1].cssselect("a")[0].text_content()
            for game_tr in game_root.cssselect("div#game_table_box table tr"):
                game_tds = game_tr.cssselect("td")
                if len(game_tds) == 5:
                    data = {
                         'Title' : title,
                         'Region' : game_tds[2].text_content(),
                         'Release_Date' : game_tds[3].text_content(),
                         'Platform' : platform,
                         'Genre' : genre,
                         'Publisher' : game_tds[1].text_content()
                    }
                    saveToStore(data)

urls = ["http://www.vgchartz.com/gamedb/?name=&publisher=&platform=PC&genre=&minSales=0&results=8000", "http://www.vgchartz.com/gamedb/?name=&publisher=&platform=X360&genre=&minSales=0&results=4000", "http://www.vgchartz.com/gamedb/?name=&publisher=&platform=PS3&genre=&minSales=0&results=4000", "http://www.vgchartz.com/gamedb/?name=&publisher=&platform=Wii&genre=&minSales=0&results=4000"]

for url in urls:
    scrapeAndSave(url)
