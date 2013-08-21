import scraperwiki
import BeautifulSoup 


#Scrap news from Japanese press 
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
    url = "https://news.google.com/news/feeds?hl=ja&ned=us&ie=UTF-8&oe=UTF-8&output=rss&q=%E3%83%8D%E3%83%83%E3%83%88%E9%81%B8%E6%8C%99"
    getGoogleFeed(url)

#List of the newspapers to search
googleNewsCustomSearchLast24()