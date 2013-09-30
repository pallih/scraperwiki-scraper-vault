import scraperwiki
import lxml.html
import random

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS usergamestates('URL' string, 'UserName' string, 'Game' string, 'HoursOnRecord' real, PRIMARY KEY('URL','Game'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO usergamestates('URL', 'UserName', 'Game', 'HoursOnRecord') VALUES (?, ?, ?, ?)", (data['URL'], data['UserName'], data['Game'], data['HoursOnRecord']))
    scraperwiki.sqlite.commit()

def checkChildNodes(html):
    root = lxml.html.fromstring(html)
    urls = []
    body = root.cssselect("div#memberList div.friendBlock_in-game")
    body = body + root.cssselect("div#memberList div.friendBlock_online")
    body = body + root.cssselect("div#memberList div.friendBlock_offline")
    for el in body:
        onclick = el.attrib['onclick']
        url = onclick[onclick.index("'")+1:onclick.rindex("'")]
        urls.append(url)
    return urls

def scrapeGame(url):
    html = scraperwiki.scrape(url+"/games?xml=1")
    root = lxml.html.fromstring(html)
    sindex = html.index("gamesList")+10
    eindex = html.rindex("gamesList")
    bodycontent = html[sindex:eindex]
    sindex = bodycontent.index("games")+6
    eindex = bodycontent.rindex("games")-2
    rows = bodycontent[sindex:eindex]
    start = rows.index("<game>")
    end = rows.index("</game>")
    glist = rows.split("<game>")
    gamestats = []
    for g in glist:
        start = g.find("<name>")
        end = g.find("</name>")
        start2 = g.find("<hoursOnRecord>")
        end2 = g.find("</hoursOnRecord>")
        if start!=-1 and end!=-1:
            name = g[start+6:end]
            game = name[9:len(name)-3]
            hours = 0.0
            if start2==-1 or end2==-1:
                hours = 0.0
            else:
                hours = float(g[start2+15:end2])
            stat = {"game":game,"hours":hours}
            gamestats.append(stat)
    return gamestats


def scrapeScores(html):
    root = lxml.html.fromstring(html)
    body = root.cssselect("div#memberList div.friendBlock_in-game")
    body = body + root.cssselect("div#memberList div.friendBlock_online")
    body = body + root.cssselect("div#memberList div.friendBlock_offline")
    print len(body)
    for el in body:
        para = el.cssselect("p")[0]
        username= para.cssselect("a")[0].text_content()
        onclick = el.attrib['onclick']
        url = onclick[onclick.index("'")+1:onclick.rindex("'")]
        gamestats = scrapeGame(url)
        for gamestat in gamestats:
            data = {
                 'URL' : url ,
                 'UserName' : username,
                 'Game': gamestat['game'],
                 'HoursOnRecord': gamestat['hours']
            }
            saveToStore(data)

def start(urls):
    urllist = []
    urllist = urls
    i = 0
    while len(urllist) != 0:
        
        index = -1
        nodes = -1
        for url in urllist:
            html = scraperwiki.scrape(url+"/friends")
            current_nodes = len(checkChildNodes(html))
            realhtml = scraperwiki.scrape(url+"")
            scrapeScores(html)
            if current_nodes > nodes:
                index = urllist.index(url)
                nodes = current_nodes
        
        #index = random.randint(0,len(urllist)-1)
        node = urllist[index]
        html = scraperwiki.scrape(node+"/friends")   
        urllist = checkChildNodes(html)
            
            

urls = ["http://steamcommunity.com/profiles/76561198007643299"];

start(urls)import scraperwiki
import lxml.html
import random

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS usergamestates('URL' string, 'UserName' string, 'Game' string, 'HoursOnRecord' real, PRIMARY KEY('URL','Game'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO usergamestates('URL', 'UserName', 'Game', 'HoursOnRecord') VALUES (?, ?, ?, ?)", (data['URL'], data['UserName'], data['Game'], data['HoursOnRecord']))
    scraperwiki.sqlite.commit()

def checkChildNodes(html):
    root = lxml.html.fromstring(html)
    urls = []
    body = root.cssselect("div#memberList div.friendBlock_in-game")
    body = body + root.cssselect("div#memberList div.friendBlock_online")
    body = body + root.cssselect("div#memberList div.friendBlock_offline")
    for el in body:
        onclick = el.attrib['onclick']
        url = onclick[onclick.index("'")+1:onclick.rindex("'")]
        urls.append(url)
    return urls

def scrapeGame(url):
    html = scraperwiki.scrape(url+"/games?xml=1")
    root = lxml.html.fromstring(html)
    sindex = html.index("gamesList")+10
    eindex = html.rindex("gamesList")
    bodycontent = html[sindex:eindex]
    sindex = bodycontent.index("games")+6
    eindex = bodycontent.rindex("games")-2
    rows = bodycontent[sindex:eindex]
    start = rows.index("<game>")
    end = rows.index("</game>")
    glist = rows.split("<game>")
    gamestats = []
    for g in glist:
        start = g.find("<name>")
        end = g.find("</name>")
        start2 = g.find("<hoursOnRecord>")
        end2 = g.find("</hoursOnRecord>")
        if start!=-1 and end!=-1:
            name = g[start+6:end]
            game = name[9:len(name)-3]
            hours = 0.0
            if start2==-1 or end2==-1:
                hours = 0.0
            else:
                hours = float(g[start2+15:end2])
            stat = {"game":game,"hours":hours}
            gamestats.append(stat)
    return gamestats


def scrapeScores(html):
    root = lxml.html.fromstring(html)
    body = root.cssselect("div#memberList div.friendBlock_in-game")
    body = body + root.cssselect("div#memberList div.friendBlock_online")
    body = body + root.cssselect("div#memberList div.friendBlock_offline")
    print len(body)
    for el in body:
        para = el.cssselect("p")[0]
        username= para.cssselect("a")[0].text_content()
        onclick = el.attrib['onclick']
        url = onclick[onclick.index("'")+1:onclick.rindex("'")]
        gamestats = scrapeGame(url)
        for gamestat in gamestats:
            data = {
                 'URL' : url ,
                 'UserName' : username,
                 'Game': gamestat['game'],
                 'HoursOnRecord': gamestat['hours']
            }
            saveToStore(data)

def start(urls):
    urllist = []
    urllist = urls
    i = 0
    while len(urllist) != 0:
        
        index = -1
        nodes = -1
        for url in urllist:
            html = scraperwiki.scrape(url+"/friends")
            current_nodes = len(checkChildNodes(html))
            realhtml = scraperwiki.scrape(url+"")
            scrapeScores(html)
            if current_nodes > nodes:
                index = urllist.index(url)
                nodes = current_nodes
        
        #index = random.randint(0,len(urllist)-1)
        node = urllist[index]
        html = scraperwiki.scrape(node+"/friends")   
        urllist = checkChildNodes(html)
            
            

urls = ["http://steamcommunity.com/profiles/76561198007643299"];

start(urls)