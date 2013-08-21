import scraperwiki
from bs4 import BeautifulSoup


def scrapeArticle(link):
    link_news = scraperwiki.scrape(link)
    soup_link = BeautifulSoup(link_news)
    title = soup_link.find("h1", attrs = {"id":"article-title", "class":"entry-title"})
    article = soup_link.find("div", attrs = {"class": "article-text KonaBody"})
    paragraphs = article.findAll("p")
    story = ""
    for paragraph in paragraphs:
        story += paragraph.getText()
    return story

def main():

    response = scraperwiki.scrape("http://www.foxnews.com/politics/index.html")
    soup = BeautifulSoup(response)
    results = soup.find("div", attrs = {"class": "dv-feature m-9 m-l t--1ms"})
    results = results.find("ul", attrs = {"class":"dv-encap"})
    results = results.findAll("li")
    for item in results:
        item = item.find("a")
        link = item.get("href")
        story = scrapeArticle(link)
        datas = {"URL":link, "Article":story}
        scraperwiki.sqlite.save(unique_keys=["URL"],data = datas)
        
main()

