import scraperwiki
import lxml.etree
import lxml.html
import urllib

def getRoot(url):
    root = lxml.html.parse(url).getroot()
    return root

def getDetailData(url):
    root = getRoot(url) 
    htmlContent = root.cssselect(".innerContainer")[0]

    return lxml.html.tostring(htmlContent)

def getRSSitems(url):

    tree = lxml.etree.parse(urllib.urlopen(url))
    items = tree.xpath("//item")

    rssArticles = []

    for item in items:
        article = {}

        article["title"] = item.xpath("./title")[0].text.strip()
        article["link"] = item.xpath("./link")[0].text.strip()
        article["guid"] = item.xpath("./guid")[0].text.strip()
        article["pubDate"] = item.xpath("./pubDate")[0].text.strip()
        article["description"] = item.xpath("./description")[0].text.strip()
        article["enclosure_url"] = item.xpath("./enclosure/@url")[0].strip()
        article["enclosure_type"] = item.xpath("./enclosure/@type")[0].strip()

        # Försök hämta HTML från detaljsidan
        # Vi parsar det senare...
        try:
            article["detail_html"] = getDetailData(article["link"])
        except:
            article["detail_html"] = None

        # Spara datan
        scraperwiki.sqlite.save(["guid"], article, verbose=2)           

    return rssArticles

rssURLs = ["http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=10&links=preserve&exc=&submit=Create+Feed",
"http://www.skandiamaklarna.se/till-salu/rss/1/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/2/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/3/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/4/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/5/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/6/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/7/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/8/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/9/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/10/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/11/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/12/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/13/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/14/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/15/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/16/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/17/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/18/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/19/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/20/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/21/all/all/all/1%2C8/0%2C300/0%2C8000000"]

for rssURL in rssURLs:
    print "Getting data from",rssURL
    try:
        getRSSitems(rssURL)
    except:
        print "could not scrape", rssURL
    import scraperwiki
import lxml.etree
import lxml.html
import urllib

def getRoot(url):
    root = lxml.html.parse(url).getroot()
    return root

def getDetailData(url):
    root = getRoot(url) 
    htmlContent = root.cssselect(".innerContainer")[0]

    return lxml.html.tostring(htmlContent)

def getRSSitems(url):

    tree = lxml.etree.parse(urllib.urlopen(url))
    items = tree.xpath("//item")

    rssArticles = []

    for item in items:
        article = {}

        article["title"] = item.xpath("./title")[0].text.strip()
        article["link"] = item.xpath("./link")[0].text.strip()
        article["guid"] = item.xpath("./guid")[0].text.strip()
        article["pubDate"] = item.xpath("./pubDate")[0].text.strip()
        article["description"] = item.xpath("./description")[0].text.strip()
        article["enclosure_url"] = item.xpath("./enclosure/@url")[0].strip()
        article["enclosure_type"] = item.xpath("./enclosure/@type")[0].strip()

        # Försök hämta HTML från detaljsidan
        # Vi parsar det senare...
        try:
            article["detail_html"] = getDetailData(article["link"])
        except:
            article["detail_html"] = None

        # Spara datan
        scraperwiki.sqlite.save(["guid"], article, verbose=2)           

    return rssArticles

rssURLs = ["http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=10&links=preserve&exc=&submit=Create+Feed",
"http://www.skandiamaklarna.se/till-salu/rss/1/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/2/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/3/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/4/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/5/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/6/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/7/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/8/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/9/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/10/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/11/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/12/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/13/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/14/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/15/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/16/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/17/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/18/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/19/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/20/all/all/all/1%2C8/0%2C300/0%2C8000000",
"http://www.skandiamaklarna.se/till-salu/rss/21/all/all/all/1%2C8/0%2C300/0%2C8000000"]

for rssURL in rssURLs:
    print "Getting data from",rssURL
    try:
        getRSSitems(rssURL)
    except:
        print "could not scrape", rssURL
    