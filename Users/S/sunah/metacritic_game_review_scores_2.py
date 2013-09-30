import scraperwiki
import lxml.html

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS metacritic ('Title' string, 'Platform' string, 'Genre' string, 'Publisher' string, 'Release_Date' string, 'Score' integer, PRIMARY KEY('Title', 'Platform'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO metacritic ('Title', 'Platform', 'Genre', 'Publisher', 'Release_Date', 'Score') VALUES (?, ?, ?, ?, ?, ?)", (data['Title'], data['Platform'], data['Genre'], data['Publisher'], data['Release_Date'], data['Score']))
    scraperwiki.sqlite.commit()

def scrapeScores(html):
    root = lxml.html.fromstring(html)
    body = root.cssselect("div.body_wrap")[0]
    for li in body.cssselect("ol li.product"):
        title = li.cssselect("h3")[0].text_content()
        platform = li.cssselect(".platform_list span.data")[0].text_content()
        genre = ""
        if len(li.cssselect(".genre span.data")) > 0:
            genre = li.cssselect(".genre span.data")[0].text_content()
        publisher = ""
        if len(li.cssselect(".publisher span.data")) > 0:
            publisher = li.cssselect(".publisher span.data")[0].text_content()
        release_date = li.cssselect(".release_date span.data")[0].text_content()
        score = li.cssselect(".std_score .score_wrap span.data")[0].text_content()
        final_score = -1
        if score != 'tbd':
            final_score = int(score)
        data = {
             'Title' : title,
             'Platform' : platform,
             'Genre' : genre,
             'Publisher' : publisher,
             'Release_Date' : release_date,
             'Score' : final_score
        }
        saveToStore(data)

def start(urls):
    for url in urls:
        current_url = url
        while current_url is not None:            
            html = scraperwiki.scrape(current_url)
            scrapeScores(html)
            root = lxml.html.fromstring(html)
            next_a = root.cssselect(".page_nav .page_flipper span.next a")
            if not next_a:
                current_url = None
            else:
                current_url = "http://www.metacritic.com" + next_a[0].attrib['href']

urls = ["http://www.metacritic.com/browse/games/title/ps3?view=detailed", "http://www.metacritic.com/browse/games/title/xbox360?view=detailed", "http://www.metacritic.com/browse/games/title/pc?view=detailed", "http://www.metacritic.com/browse/games/title/wii?view=detailed"];

start(urls)import scraperwiki
import lxml.html

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS metacritic ('Title' string, 'Platform' string, 'Genre' string, 'Publisher' string, 'Release_Date' string, 'Score' integer, PRIMARY KEY('Title', 'Platform'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO metacritic ('Title', 'Platform', 'Genre', 'Publisher', 'Release_Date', 'Score') VALUES (?, ?, ?, ?, ?, ?)", (data['Title'], data['Platform'], data['Genre'], data['Publisher'], data['Release_Date'], data['Score']))
    scraperwiki.sqlite.commit()

def scrapeScores(html):
    root = lxml.html.fromstring(html)
    body = root.cssselect("div.body_wrap")[0]
    for li in body.cssselect("ol li.product"):
        title = li.cssselect("h3")[0].text_content()
        platform = li.cssselect(".platform_list span.data")[0].text_content()
        genre = ""
        if len(li.cssselect(".genre span.data")) > 0:
            genre = li.cssselect(".genre span.data")[0].text_content()
        publisher = ""
        if len(li.cssselect(".publisher span.data")) > 0:
            publisher = li.cssselect(".publisher span.data")[0].text_content()
        release_date = li.cssselect(".release_date span.data")[0].text_content()
        score = li.cssselect(".std_score .score_wrap span.data")[0].text_content()
        final_score = -1
        if score != 'tbd':
            final_score = int(score)
        data = {
             'Title' : title,
             'Platform' : platform,
             'Genre' : genre,
             'Publisher' : publisher,
             'Release_Date' : release_date,
             'Score' : final_score
        }
        saveToStore(data)

def start(urls):
    for url in urls:
        current_url = url
        while current_url is not None:            
            html = scraperwiki.scrape(current_url)
            scrapeScores(html)
            root = lxml.html.fromstring(html)
            next_a = root.cssselect(".page_nav .page_flipper span.next a")
            if not next_a:
                current_url = None
            else:
                current_url = "http://www.metacritic.com" + next_a[0].attrib['href']

urls = ["http://www.metacritic.com/browse/games/title/ps3?view=detailed", "http://www.metacritic.com/browse/games/title/xbox360?view=detailed", "http://www.metacritic.com/browse/games/title/pc?view=detailed", "http://www.metacritic.com/browse/games/title/wii?view=detailed"];

start(urls)