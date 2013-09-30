import scraperwiki
import lxml.html

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS metacritic ('Title' string, 'Prodco' string, 'Rating' string, 'Run_Time' string, 'Release_Date' string, 'Score' integer, PRIMARY KEY('Title', 'Prodco'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO metacritic ('Title', 'Prodco', 'Rating', 'Run_Time', 'Release_Date', 'Score') VALUES (?, ?, ?, ?, ?, ?)", (data['Title'], data['Prodco'], data['Rating'], data['Run_Time'], data['Release_Date'], data['Score']))
    scraperwiki.sqlite.commit()

def scrapeScores(html):
    root = lxml.html.fromstring(html)
    body = root.cssselect("div.body_wrap")[0]
    for li in body.cssselect("ol li.product"):
        title = li.cssselect("h3")[0].text_content()
        prodco = li.cssselect(".developer span.data")[0].text_content()
        rating = ""
        if len(li.cssselect(".rating span.data")) > 0:
            rating = li.cssselect(".rating span.data")[0].text_content()
        run_time = ""
        if len(li.cssselect(".runtime span.data")) > 0:
            run_time = li.cssselect(".runtime span.data")[0].text_content()
        release_date = li.cssselect(".release_date span.data")[0].text_content()
        score = li.cssselect(".std_score .score_wrap span.data")[0].text_content()
        final_score = -1
        if score != 'tbd':
            final_score = int(score)
        data = {
             'Title' : title,
             'Prodco' : prodco,
             'Rating' : rating,
             'Run_Time' : run_time,
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

urls = ["http://www.metacritic.com/browse/dvds/release-date/new-releases/metascore?view=detailed"];

start(urls)import scraperwiki
import lxml.html

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS metacritic ('Title' string, 'Prodco' string, 'Rating' string, 'Run_Time' string, 'Release_Date' string, 'Score' integer, PRIMARY KEY('Title', 'Prodco'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO metacritic ('Title', 'Prodco', 'Rating', 'Run_Time', 'Release_Date', 'Score') VALUES (?, ?, ?, ?, ?, ?)", (data['Title'], data['Prodco'], data['Rating'], data['Run_Time'], data['Release_Date'], data['Score']))
    scraperwiki.sqlite.commit()

def scrapeScores(html):
    root = lxml.html.fromstring(html)
    body = root.cssselect("div.body_wrap")[0]
    for li in body.cssselect("ol li.product"):
        title = li.cssselect("h3")[0].text_content()
        prodco = li.cssselect(".developer span.data")[0].text_content()
        rating = ""
        if len(li.cssselect(".rating span.data")) > 0:
            rating = li.cssselect(".rating span.data")[0].text_content()
        run_time = ""
        if len(li.cssselect(".runtime span.data")) > 0:
            run_time = li.cssselect(".runtime span.data")[0].text_content()
        release_date = li.cssselect(".release_date span.data")[0].text_content()
        score = li.cssselect(".std_score .score_wrap span.data")[0].text_content()
        final_score = -1
        if score != 'tbd':
            final_score = int(score)
        data = {
             'Title' : title,
             'Prodco' : prodco,
             'Rating' : rating,
             'Run_Time' : run_time,
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

urls = ["http://www.metacritic.com/browse/dvds/release-date/new-releases/metascore?view=detailed"];

start(urls)