import scraperwiki
import BeautifulSoup 


#Scrap news from Japanese press 
def getHatenaFeed(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    tags = soup.findAll("item")

    for d in tags:
        try:
            title = d.find("title").getText()
            link = d.find("link").getText()
            description = d.find("description").getText()
            pubdate = str(d).split("<dc:date>")[1].split("</dc:date>")[0]
            data = {"title":title,"description":description,"link":link,"pubdate":pubdate}
            scraperwiki.sqlite.save(unique_keys=['link'],data=data)
        except:
            pass

def HatenaNewsCustomSearchLast24():
    url = "http://b.hatena.ne.jp/search/tag?q=%E3%83%8D%E3%83%83%E3%83%88%E9%81%B8%E6%8C%99&users=1&mode=rss"
    getHatenaFeed(url)

#List of the newspapers to search
HatenaNewsCustomSearchLast24()import scraperwiki
import BeautifulSoup 


#Scrap news from Japanese press 
def getHatenaFeed(url):
    html = scraperwiki.scrape(url)
    soup = BeautifulSoup.BeautifulSoup(html)
    tags = soup.findAll("item")

    for d in tags:
        try:
            title = d.find("title").getText()
            link = d.find("link").getText()
            description = d.find("description").getText()
            pubdate = str(d).split("<dc:date>")[1].split("</dc:date>")[0]
            data = {"title":title,"description":description,"link":link,"pubdate":pubdate}
            scraperwiki.sqlite.save(unique_keys=['link'],data=data)
        except:
            pass

def HatenaNewsCustomSearchLast24():
    url = "http://b.hatena.ne.jp/search/tag?q=%E3%83%8D%E3%83%83%E3%83%88%E9%81%B8%E6%8C%99&users=1&mode=rss"
    getHatenaFeed(url)

#List of the newspapers to search
HatenaNewsCustomSearchLast24()