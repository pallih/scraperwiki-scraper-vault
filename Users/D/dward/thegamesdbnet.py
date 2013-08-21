import scraperwiki
import lxml.html

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS gamesdb ('Title' string, 'Platform' string, 'Publisher' string, 'Genres' string, PRIMARY KEY('Title', 'Platform'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO gamesdb ('Title', 'Platform', 'Publisher', 'Genres') VALUES (?, ?, ?, ?)", (data['Title'], data['Platform'], data['Publisher'], data['Genres']))
    scraperwiki.sqlite.commit()


def scrape(url):
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    for tr in root.cssselect("table#listtable tr"):
        tds = tr.cssselect("td")
        if tds[0].text_content() == 'ID':
            continue
        game_url = tds[1].cssselect("a")[0].attrib["href"]
        game_html = scraperwiki.scrape(game_url)
        game_root = lxml.html.fromstring(game_html)
        title = game_root.cssselect("div#gameTitle h1")[0].text_content()
        platform = game_root.cssselect("div#gameInfo h2 a")[0].text_content()
        publisher = ""
        details = game_root.cssselect("div#gameVitals p")[0].text_content()
        genres_index = details.find('Genres')
        release_date_index = details.find('Release Date')
        genres = game_root.cssselect("div#gameVitals p")[0].text_content()[genres_index + 7 : release_date_index].strip()
        if len(game_root.cssselect("div#gameVitals p img")) == 1:
            publisher = game_root.cssselect("div#gameVitals p img")[0].attrib["title"]
        elif len(game_root.cssselect("div#gameVitals p img")) == 2:
            publisher = game_root.cssselect("div#gameVitals p img")[1].attrib["title"]
        else:
            publisher_index = details.find("Publisher")
            if(publisher_index != -1):
                publisher = details[publisher_index + 10:].strip()
        data = {
            'Title' : title,
            'Platform' : platform,
            'Publisher' : publisher,
            'Genres' : genres
        }
        saveToStore(data)
    
def start():
    urls = {'http://thegamesdb.net/browse/12/?searchview=table&function=Browse%20By%20Platform&sortBy=&limit=4000&page=1&updateview=yes','http://thegamesdb.net/browse/15/?searchview=table&function=Browse%20By%20Platform&sortBy=&limit=4000&page=1&updateview=yes','http://thegamesdb.net/browse/1/?searchview=table&function=Browse%20By%20Platform&sortBy=&limit=4000&page=1&updateview=yes','http://thegamesdb.net/browse/9/?searchview=table&function=Browse%20By%20Platform&sortBy=&limit=4000&page=1&updateview=yes'}
    for url in urls:
        scrape(url)

start()