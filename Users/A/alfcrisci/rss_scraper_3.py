import scraperwiki
import lxml.etree
import lxml.html
import urllib

def getRoot(url):
    root = lxml.html.parse(url).getroot()
    return root

def getRSSitems(url):

    tree = lxml.etree.parse(urllib.urlopen(url[0]))
    items = tree.xpath("//item")

    newspaper = url[1]
    print newspaper

    rssArticles = []

    for item in items:
        article = {}

        article["title"] = item.xpath("./title")[0].text.strip()
        article["link"] = item.xpath("./link")[0].text.strip()
        article["description"] = item.xpath("./description")[0].text.strip()
        article["pubDate"] = item.xpath("./pubDate")[0].text.strip()
        article["category"] = item.xpath("./category")[0].text.strip()
        article["category1"] = item.xpath("./category")[1].text.strip()
        article["category2"] = item.xpath("./category")[2].text.strip()
        article["category3"] = item.xpath("./category")[3].text.strip()
        article["guid"] = item.xpath("./guid")[0].text.strip()

        article["articleId"] = int(article["guid"].split("=")[1])
        description = item.xpath("./description")
        if(len(description) > 0):
            article["description"] = description[0].text.strip()

        scraperwiki.sqlite.save(unique_keys=['articleId'], data=article)
               

        rssArticles.append(article)

    return rssArticles

rssURLs = [("http://www.cyberwarnews.info/feed/","")]

for rssURL in rssURLs:
    print "Getting data from",rssURL
    getRSSitems(rssURL)

import scraperwiki
import lxml.etree
import lxml.html
import urllib

def getRoot(url):
    root = lxml.html.parse(url).getroot()
    return root

def getRSSitems(url):

    tree = lxml.etree.parse(urllib.urlopen(url[0]))
    items = tree.xpath("//item")

    newspaper = url[1]
    print newspaper

    rssArticles = []

    for item in items:
        article = {}

        article["title"] = item.xpath("./title")[0].text.strip()
        article["link"] = item.xpath("./link")[0].text.strip()
        article["description"] = item.xpath("./description")[0].text.strip()
        article["pubDate"] = item.xpath("./pubDate")[0].text.strip()
        article["category"] = item.xpath("./category")[0].text.strip()
        article["category1"] = item.xpath("./category")[1].text.strip()
        article["category2"] = item.xpath("./category")[2].text.strip()
        article["category3"] = item.xpath("./category")[3].text.strip()
        article["guid"] = item.xpath("./guid")[0].text.strip()

        article["articleId"] = int(article["guid"].split("=")[1])
        description = item.xpath("./description")
        if(len(description) > 0):
            article["description"] = description[0].text.strip()

        scraperwiki.sqlite.save(unique_keys=['articleId'], data=article)
               

        rssArticles.append(article)

    return rssArticles

rssURLs = [("http://www.cyberwarnews.info/feed/","")]

for rssURL in rssURLs:
    print "Getting data from",rssURL
    getRSSitems(rssURL)

