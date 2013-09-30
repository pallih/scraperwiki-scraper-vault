import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime




def strip_tags(html):
    return ' '.join(html.findAll(text=True))


masterletter = "a"
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
pagenum = ["1", "2", "3", "4", "5"]

for i in range(len(alphabet)):       

    for p in range(len(pagenum)):

        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3D", masterletter, alphabet[i], "&max=300&paged=", pagenum[p], "&submit=Create+Feed&links=preserve"]
        source = "".join(sourcearray)


        html = scraperwiki.scrape(source)                                       #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup                                                     
        items = soup.findAll('item')                                            #print type(items) #print items[0]

        article = {}          

        for item in items:
            article['title'] = item.find('title').text
            article['url'] = item.find('link').next                                
            article['description'] = item.find('description').text
            article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
            article['now'] = datetime.now()
            print article         
            scraperwiki.sqlite.save(['now'], article)
import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime




def strip_tags(html):
    return ' '.join(html.findAll(text=True))


masterletter = "a"
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
pagenum = ["1", "2", "3", "4", "5"]

for i in range(len(alphabet)):       

    for p in range(len(pagenum)):

        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3D", masterletter, alphabet[i], "&max=300&paged=", pagenum[p], "&submit=Create+Feed&links=preserve"]
        source = "".join(sourcearray)


        html = scraperwiki.scrape(source)                                       #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup                                                     
        items = soup.findAll('item')                                            #print type(items) #print items[0]

        article = {}          

        for item in items:
            article['title'] = item.find('title').text
            article['url'] = item.find('link').next                                
            article['description'] = item.find('description').text
            article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
            article['now'] = datetime.now()
            print article         
            scraperwiki.sqlite.save(['now'], article)
