import scraperwiki
import lxml.html
import random

def saveToStore(data):
    scraperwiki.sqlite.execute("CREATE TABLE IF NOT EXISTS userpages('URL' string, 'UserName' string, PRIMARY KEY('URL'))")
    scraperwiki.sqlite.execute("INSERT OR REPLACE INTO userpages('URL', 'UserName') VALUES (?, ?)", (data['URL'], data['UserName']))
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
        data = {
             'URL' : url ,
             'UserName' : username
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
            scrapeScores(html)
            if current_nodes > nodes:
                index = urllist.index(url)
                nodes = current_nodes
        
        #index = random.randint(0,len(urllist)-1)
        node = urllist[index]
        html = scraperwiki.scrape(node+"/friends")   
        urllist = checkChildNodes(html)
            
            

urls = ["http://steamcommunity.com/profiles/76561198087603531"];

start(urls)