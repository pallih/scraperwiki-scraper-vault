import scraperwiki
import lxml.etree
import lxml.html
import urllib


def getRoot(url):
    root = lxml.html.parse(url).getroot()
    return root

def getRSSitems(url):

    tree = lxml.etree.parse(urllib.urlopen(url))
    items = tree.xpath('//item')

    rssArticles = []

    for item in items:
        article = {}

        article["title"] = item.xpath("./title")[0].text.strip()
        article["link"] = item.xpath("./link")[0].text.strip()
        article["author"] = item.xpath("./author")[0].text.strip()
        article["pubDate"] = item.xpath("./pubDate")[0].text.strip()

        # Hämta artikel ID fråm länken samt en tagg
        article["articleId"] = int(article["link"].split("=")[1])

        # Kolla om det kommer från PT noje, sätt rätt tagg då.
        if(article["link"].find('http://www.ptnoje.se') < 0):
            article["tag"] = article["link"].split("/")[3].strip()
        else:
            article["tag"] = "noje"

        # Alla har inte beskrivningar så vi kollar här
        description = item.xpath("./description")
        if(len(description) > 0):
            article["description"] = description[0].text.strip()

        # Försök hämta hela artikele
        try:
            fullArticle = getFullArticle(article["link"])
            article["articleHeader"] = fullArticle["articleHeader"]
            article["articleLabel"] = fullArticle["articleLabel"] 
            article["articlePreamble"] = fullArticle["articlePreamble"] 
            article["articleBodyText"] = fullArticle["articleBodyText"]
        except:
            print "Problem att hämta hela artikeln vid url:", article["link"]
            pass   

        # Spara datan
        scraperwiki.sqlite.save(unique_keys=["articleId"], data=article)

        rssArticles.append(article)
        
    return rssArticles


def getFullArticle(url):
    articleRoot = getRoot(url)
    fullArticle = {}

    if(url.find('http://www.ptnoje.se') < 0):

#        fullArticle["articleHeader"] = articleRoot.cssselect("span.Rub1")[0].text.strip()
#        fullArticle["articleLabel"] = articleRoot.cssselect("span.ArticleLabel")[0].text.strip()
#        fullArticle["articlePreamble"] = articleRoot.cssselect("span.ArticleLabel")[0].tail.strip()

        articleHeader = articleRoot.cssselect("span.Rub1")
        if(len(articleHeader) > 0):
            fullArticle["articleHeader"] = articleHeader[0].text.strip()
        else:
            fullArticle["articleHeader"] = ""    

        articleLabel = articleRoot.cssselect("span.ArticleLabel")
        if(len(articleLabel) > 0):
            fullArticle["articleLabel"] = articleLabel[0].text.strip()
        else:
            fullArticle["articleLabel"] = ""    

        articlePreamble = articleRoot.cssselect("span.ArticleLabel")
        if(len(articlePreamble) > 0):
            fullArticle["articlePreamble"] = articlePreamble[0].tail.strip()
        else:
            fullArticle["articlePreamble"] = ""    

        bodytext = articleRoot.cssselect("div.Btex")
        if(len(bodytext) > 0):
            fullArticle["articleBodyText"] = bodytext[0].text_content().strip()
        else:
            fullArticle["articleBodyText"] = ""    

    else:

        fullArticle["articleHeader"] = articleRoot.cssselect("h2 strong")[0].text.strip()

        articlePreamble = articleRoot.cssselect("div.Ingress b")
        if(len(articlePreamble) > 0):
            fullArticle["articlePreamble"] = articlePreamble[0].text_content().strip()
        else:
            fullArticle["articlePreamble"] = ""

        articleLabel = articleRoot.cssselect("span.Label")
        if(len(articleLabel) > 0):
            fullArticle["articleLabel"] = articleLabel[0].text.strip()
        else:
            fullArticle["articleLabel"] = ""

        bodytext = articleRoot.cssselect("div#ctl00_cphMainContent_Article_pnlBtex")
        if(len(bodytext) > 0):
            fullArticle["articleBodyText"] = bodytext[0].text_content().strip()
        else:
            fullArticle["articleBodyText"] = ""    

    return fullArticle

rssURLs = ["http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daz&max=100&links=preserve&exc=&submit=Create+Feed",
"http://www.pitea-tidningen.se/nyheter.rss",
"http://www.pitea-tidningen.se/sport.rss",
"http://www.pitea-tidningen.se/noje.rss",
"http://www.pitea-tidningen.se/kultur.rss",
"http://www.pitea-tidningen.se/familjenytt.rss",
"http://www.pitea-tidningen.se/debatt.rss",
"http://www.pitea-tidningen.se/ledare.rss",
"http://www.pitea-tidningen.se/pitea.rss",
"http://www.pitea-tidningen.se/arjeplog.rss",
"http://www.pitea-tidningen.se/arvidsjaur.rss",
"http://www.pitea-tidningen.se/alvsbyn.rss",
"http://www.pitea-tidningen.se/lulea.rss",
"http://www.pitea-tidningen.se/boden.rss",
"http://www.pitea-tidningen.se/skelleftea.rss",
"http://www.pitea-tidningen.se/kalix.rss",
"http://www.pitea-tidningen.se/haparanda.rss",
"http://www.pitea-tidningen.se/gallivare.rss",
"http://www.pitea-tidningen.se/kiruna.rss",
"http://www.pitea-tidningen.se/malmberget.rss",
"http://www.pitea-tidningen.se/jokkmokk.rss",
"http://www.pitea-tidningen.se/pajala.rss",
"http://www.pitea-tidningen.se/overkalix.rss",
"http://www.pitea-tidningen.se/overtornea.rss",
"http://www.pitea-tidningen.se/umea.rss"]

testRSS = ["http://www.pitea-tidningen.se/noje.rss"]

#fullArticle = getFullArticle("http://www.pitea-tidningen.se/pitea/artikel.aspx?ArticleId=6974134")
#print fullArticle

for rssURL in rssURLs:
    pass
    print "Getting data from",rssURL
    getRSSitems(rssURL)
