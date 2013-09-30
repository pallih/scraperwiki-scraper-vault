import scraperwiki
import BeautifulSoup 


#Scrap news from spanish press 
def getGoogleFeed(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    news = soup.findAll("item")
    for d in news:
        try:
            title = d.find("title").getText()
            link = d.getText().split("url=")[1].split("tag:")[0]
            description = d.find("description").getText()
            pubdate = str(d).split("<pubdate>")[1].split("</pubdate>")[0]
            data = {"title":title,"description":description,"link":link,"pubdate":pubdate}
            scraperwiki.sqlite.save(unique_keys=['link'],data=data)
        except:
            pass

def googleNewsCustomSearchLast24():
    url = "http://news.google.es/news?gl=es&hl=es&as_occt=any&as_qdr=d&authuser=0&q=pah&um=1&ie=UTF-8&output=rss"
    getGoogleFeed(url)

#List of the newspapers to search
googleNewsCustomSearchLast24()import scraperwiki
import BeautifulSoup 


#Scrap news from spanish press 
def getGoogleFeed(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    news = soup.findAll("item")
    for d in news:
        try:
            title = d.find("title").getText()
            link = d.getText().split("url=")[1].split("tag:")[0]
            description = d.find("description").getText()
            pubdate = str(d).split("<pubdate>")[1].split("</pubdate>")[0]
            data = {"title":title,"description":description,"link":link,"pubdate":pubdate}
            scraperwiki.sqlite.save(unique_keys=['link'],data=data)
        except:
            pass

def googleNewsCustomSearchLast24():
    url = "http://news.google.es/news?gl=es&hl=es&as_occt=any&as_qdr=d&authuser=0&q=pah&um=1&ie=UTF-8&output=rss"
    getGoogleFeed(url)

#List of the newspapers to search
googleNewsCustomSearchLast24()