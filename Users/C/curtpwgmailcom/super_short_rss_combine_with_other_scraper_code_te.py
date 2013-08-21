import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime
from urllib import urlopen


def strip_tags(html):
    return ' '.join(html.findAll(text=True))


masterletter = "a"
alphabet = ["a","b"]
pagenum = ["1", "2"]

for j in range(len(alphabet)):       

    for p in range(len(pagenum)):

        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3D", masterletter, alphabet[j], "&max=50&paged=", pagenum[p], "&submit=Create+Feed&links=preserve"]
        source = "".join(sourcearray)

        html = scraperwiki.scrape(source)                                       #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup                                                     
        items = soup.findAll('item')                                            #print type(items) #print items[0]

                 
        for i in range(len(items)):
            article = {} 
            item = items[i]
            article['title'] = item.find('title').text
            article['url'] = item.find('link').next                                
            article['description'] = item.find('description').text
            article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
            article['now'] = datetime.now()
            print article         
        #    scraperwiki.sqlite.save(['title'], article)
        #    articletemp = [article['title'], article['url'], article['description'], article['pubdate'], article['now']]
            scraperwiki.sqlite.save(unique_keys=['title'], article)
        #    print scraperwiki.sqlite.table_info("swdata")
