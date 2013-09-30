import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime




def strip_tags(html):
    return ' '.join(html.findAll(text=True))


#masterletter = "e"
fedsearchnum = ["2587594", 
"2587611", 
"2587616", 
"2587619", 
"2587621", 
"2587626", 
"2587631", 
"2587645", 
"2587649", 
"2587656"]
#, 
#"k", 
#"l", 
#"m", 
#"n", 
#"o", 
#"p", 
#"q", 
#"r", 
#"s", 
#"q", 
#"r", 
#"s", 
#"t", 
#"u", 
#"v", 
#"w", 
#"x", 
#"y", 
#"z"]

pagenum = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

for i in range(len(fedsearchnum)):       

    for p in range(len(pagenum)):

#http://www.jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FRSSFeed%2F2587594&max=20&links=preserve&exc=&submit=Create+Feed

#http://jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FRSSFeed%2F2568847&max=10&submit=Create+Feed&links=preserve

        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FRSSFeed%2F", fedsearchnum[i], "&max=20&paged=", pagenum[p], "&links=preserve&exc=&submit=Create+Feed"]

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


#masterletter = "e"
fedsearchnum = ["2587594", 
"2587611", 
"2587616", 
"2587619", 
"2587621", 
"2587626", 
"2587631", 
"2587645", 
"2587649", 
"2587656"]
#, 
#"k", 
#"l", 
#"m", 
#"n", 
#"o", 
#"p", 
#"q", 
#"r", 
#"s", 
#"q", 
#"r", 
#"s", 
#"t", 
#"u", 
#"v", 
#"w", 
#"x", 
#"y", 
#"z"]

pagenum = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

for i in range(len(fedsearchnum)):       

    for p in range(len(pagenum)):

#http://www.jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FRSSFeed%2F2587594&max=20&links=preserve&exc=&submit=Create+Feed

#http://jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FRSSFeed%2F2568847&max=10&submit=Create+Feed&links=preserve

        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=https%3A%2F%2Fwww.usajobs.gov%2FJobSearch%2FSearch%2FRSSFeed%2F", fedsearchnum[i], "&max=20&paged=", pagenum[p], "&links=preserve&exc=&submit=Create+Feed"]

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
