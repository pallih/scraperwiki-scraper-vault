import scraperwiki
import lxml.html

def saveToStore(data):
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO metacritic ('Platform', 'Title', 'Publisher', 'Release_Date', 'Score') VALUES (?, ?, ?, ?, ?)", (data['Platform'], data['Title'], data['Publisher'], data['Release_Date'], data['Score']))

def scrapeScores(html,system):
    root = lxml.html.fromstring(html)
    body = root.cssselect("div.body_wrap")[0]
    for li in body.cssselect("ol li.product"):
        title = li.cssselect("h3")[0].text_content()
        platform = system
        publisher = ""
        if len(li.cssselect(".publisher span.data")) > 0:
            publisher = li.cssselect(".publisher span.data")[0].text_content()
        release_date = li.cssselect(".release_date span.data")[0].text_content()
        score = li.cssselect(".std_score .score_wrap span.data")[0].text_content()
        final_score = -1
        if score != 'tbd':
            final_score = int(score)
        data = {
             'Platform' : platform,
             'Title' : title,
             'Publisher' : publisher,
             'Release_Date' : release_date,
             'Score' : final_score
        }
        saveToStore(data)

def process(url,system):
    current_url = url
    page_count = 1
    while current_url is not None:            
        html = scraperwiki.scrape(current_url)
        scrapeScores(html,system)
        root = lxml.html.fromstring(html)
        page_count += 1
        if page_count > max_pages:
            current_url = None
        else:
            next_a = root.cssselect(".page_nav .page_flipper span.next a")
            if not next_a:
                current_url = None
            else:
                current_url = "http://www.metacritic.com" + next_a[0].attrib['href']

def start(systems):
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS metacritic")

    scraperwiki.sqlite.execute("CREATE TABLE metacritic ('Platform' string, 'Title' string, 'Publisher' string, 'Release_Date' string, 'Score' integer, PRIMARY KEY('Title','Platform'))")

    for system in systems:
        released = "http://www.metacritic.com/browse/games/release-date/available/%s/date?view=detailed" % system
        process(released,system)
        released = "http://www.metacritic.com/browse/games/release-date/coming-soon/%s/date?view=detailed" % system
        process(released,system)

    scraperwiki.sqlite.commit()


systems = ["wii-u","ps3","xbox360","wii","3ds","ds","vita","psp"];
max_pages = 1

start(systems)import scraperwiki
import lxml.html

def saveToStore(data):
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO metacritic ('Platform', 'Title', 'Publisher', 'Release_Date', 'Score') VALUES (?, ?, ?, ?, ?)", (data['Platform'], data['Title'], data['Publisher'], data['Release_Date'], data['Score']))

def scrapeScores(html,system):
    root = lxml.html.fromstring(html)
    body = root.cssselect("div.body_wrap")[0]
    for li in body.cssselect("ol li.product"):
        title = li.cssselect("h3")[0].text_content()
        platform = system
        publisher = ""
        if len(li.cssselect(".publisher span.data")) > 0:
            publisher = li.cssselect(".publisher span.data")[0].text_content()
        release_date = li.cssselect(".release_date span.data")[0].text_content()
        score = li.cssselect(".std_score .score_wrap span.data")[0].text_content()
        final_score = -1
        if score != 'tbd':
            final_score = int(score)
        data = {
             'Platform' : platform,
             'Title' : title,
             'Publisher' : publisher,
             'Release_Date' : release_date,
             'Score' : final_score
        }
        saveToStore(data)

def process(url,system):
    current_url = url
    page_count = 1
    while current_url is not None:            
        html = scraperwiki.scrape(current_url)
        scrapeScores(html,system)
        root = lxml.html.fromstring(html)
        page_count += 1
        if page_count > max_pages:
            current_url = None
        else:
            next_a = root.cssselect(".page_nav .page_flipper span.next a")
            if not next_a:
                current_url = None
            else:
                current_url = "http://www.metacritic.com" + next_a[0].attrib['href']

def start(systems):
    scraperwiki.sqlite.execute("DROP TABLE IF EXISTS metacritic")

    scraperwiki.sqlite.execute("CREATE TABLE metacritic ('Platform' string, 'Title' string, 'Publisher' string, 'Release_Date' string, 'Score' integer, PRIMARY KEY('Title','Platform'))")

    for system in systems:
        released = "http://www.metacritic.com/browse/games/release-date/available/%s/date?view=detailed" % system
        process(released,system)
        released = "http://www.metacritic.com/browse/games/release-date/coming-soon/%s/date?view=detailed" % system
        process(released,system)

    scraperwiki.sqlite.commit()


systems = ["wii-u","ps3","xbox360","wii","3ds","ds","vita","psp"];
max_pages = 1

start(systems)