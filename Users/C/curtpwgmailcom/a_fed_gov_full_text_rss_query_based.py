import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime
import re




def strip_tags(html):
    return ' '.join(html.findAll(text=True))


masterletter = "a"
alphabet = ["a", "b", "c", "d"]
#, "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
pagenum = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

for i in range(len(alphabet)):       

    for p in range(len(pagenum)):

#http://www.jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FGetPageResults%3Fpage%3D2%26keyword%3Dj%26statusFilter%3Dpublic&max=2000&links=preserve&exc=&submit=Create+Feed

        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FGetPageResults%3Fpage%3D", pagenum[p],"%26keyword%3D", masterletter, alphabet[i], "%26statusFilter%3Dpublic&max=90&links=preserve&exc=&submit=Create+Feed"]
        source = "".join(sourcearray)


        html = scraperwiki.scrape(source)                                       #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup                                                     
        items = soup.findAll('item')                                            #print type(items) #print items[0]

        article = {}          

        for item in items:           
        
            
            print item


            article['title'] = item.find('title').text
            article['url'] = item.find('link').next                                
            article['description'] = item.find('description').text
      #      article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
            article['now'] = datetime.now()
            print article         
            scraperwiki.sqlite.save(['now'], article)
import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime
import re




def strip_tags(html):
    return ' '.join(html.findAll(text=True))


masterletter = "a"
alphabet = ["a", "b", "c", "d"]
#, "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
pagenum = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

for i in range(len(alphabet)):       

    for p in range(len(pagenum)):

#http://www.jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FGetPageResults%3Fpage%3D2%26keyword%3Dj%26statusFilter%3Dpublic&max=2000&links=preserve&exc=&submit=Create+Feed

        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FGetPageResults%3Fpage%3D", pagenum[p],"%26keyword%3D", masterletter, alphabet[i], "%26statusFilter%3Dpublic&max=90&links=preserve&exc=&submit=Create+Feed"]
        source = "".join(sourcearray)


        html = scraperwiki.scrape(source)                                       #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup                                                     
        items = soup.findAll('item')                                            #print type(items) #print items[0]

        article = {}          

        for item in items:           
        
            
            print item


            article['title'] = item.find('title').text
            article['url'] = item.find('link').next                                
            article['description'] = item.find('description').text
      #      article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
            article['now'] = datetime.now()
            print article         
            scraperwiki.sqlite.save(['now'], article)
