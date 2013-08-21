import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime
import re



def strip_tags(html):
    return ' '.join(html.findAll(text=True))


masterletter = "r"
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
pagenum = ["1", "2", "3", "4", "5", "6"]

for i in range(len(alphabet)):       

    for p in range(len(pagenum)):

        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3D", masterletter, alphabet[i], "&max=100&paged=", pagenum[p], "&submit=Create+Feed&links=preserve"]

        source = "".join(sourcearray)


        html = scraperwiki.scrape(source)                                       #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup                                                     
        items = soup.findAll('item')                                            #print type(items) #print items[0]

        article = {}          
        now = {}
        last = {}
        lastlast = {}
        lastlastlast = {}

        for item in items:
            now = item.find('title').text
            if now != last:
                if now != lastlast:
                    if now != lastlastlast:
                        article['title'] = item.find('title').text
                        article['title'] = re.sub(r'\[|\]|\s*<[^>]*>\s*', ' ', article['title'])

                        article['url'] = item.find('link').next      
                          
                        article['description'] = item.find('description').text
                        article['description'] = re.sub(r'\[|\]|\s*<[^>]*>\s*', ' ', article['description'])

                        article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)   
                        article['now'] = datetime.now()        
                        print article         
                        scraperwiki.sqlite.save(['now'], article)
                        last = now
                        lastlast = last
                        lastlastlast = lastlast