import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime




def strip_tags(html):
    return ' '.join(html.findAll(text=True))

sources  = ['http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dab&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dac&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dad&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dae&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daf&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dag&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dah&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dai&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daj&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dak&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dal&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dam&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dan&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dao&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dap&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daq&max=90&links=preserve&exc=&submit=Create+Feed',
   http://rss.indeed.com/rss?q=as http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dar&max=80&links=preserve&exc=&submit=Create+Feed',

http://rss.indeed.com/rss?q=aa
http://rss.indeed.com/rss?q=ab
http://rss.indeed.com/rss?q=ac
http://rss.indeed.com/rss?q=ad
http://rss.indeed.com/rss?q=ae
http://rss.indeed.com/rss?q=af
http://rss.indeed.com/rss?q=ag
http://rss.indeed.com/rss?q=ah
http://rss.indeed.com/rss?q=ai
http://rss.indeed.com/rss?q=aj
http://rss.indeed.com/rss?q=ak
http://rss.indeed.com/rss?q=al
http://rss.indeed.com/rss?q=am
http://rss.indeed.com/rss?q=an
http://rss.indeed.com/rss?q=ao
http://rss.indeed.com/rss?q=ap
http://rss.indeed.com/rss?q=aq
http://rss.indeed.com/rss?q=ar
http://rss.indeed.com/rss?q=as   
http://rss.indeed.com/rss?q=at
http://rss.indeed.com/rss?q=au
http://rss.indeed.com/rss?q=av
http://rss.indeed.com/rss?q=aw
http://rss.indeed.com/rss?q=ax
http://rss.indeed.com/rss?q=ay
http://rss.indeed.com/rss?q=az

 
  a b c d e f g h i j k l m n. o p q r s t u v w x y ...
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daz&max=90&links=preserve&exc=&submit=Create+Feed']

# sample URL http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=30&paged=4&submit=Create+Feed&links=preserve

masterletter = "a"
alphabet = ["a","b","c","d","e","f","g"]
pagenum = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

for i in range(len(alphabet)):       

    for p in range(len(pagenum)):

#        source = "http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3D" += masterletter += alphabet[i] "&max=30&paged=" += pagenum[p] += "&submit=Create+Feed&links=preserve"

        source = "http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=30&paged=4&submit=Create+Feed&links=preserve"

        html = scraperwiki.scrape(source)        #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup
        items = soup.findAll('item')             #print type(items) #print items[0]


        article = {}

        for item in items:
            article['title'] = item.find('title').text
            article['url'] = item.find('link').next # wow, this worked!
            article['ingress'] = item.find('description').text
            article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
            article['now'] = datetime.now()
            print article
            # the sensfull thing here would be to build a func to scrape the url form here.

        scraperwiki.sqlite.save(['title'], article)
import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime




def strip_tags(html):
    return ' '.join(html.findAll(text=True))

sources  = ['http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dab&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dac&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dad&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dae&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daf&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dag&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dah&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dai&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daj&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dak&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dal&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dam&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dan&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dao&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dap&max=90&links=preserve&exc=&submit=Create+Feed',
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daq&max=90&links=preserve&exc=&submit=Create+Feed',
   http://rss.indeed.com/rss?q=as http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Dar&max=80&links=preserve&exc=&submit=Create+Feed',

http://rss.indeed.com/rss?q=aa
http://rss.indeed.com/rss?q=ab
http://rss.indeed.com/rss?q=ac
http://rss.indeed.com/rss?q=ad
http://rss.indeed.com/rss?q=ae
http://rss.indeed.com/rss?q=af
http://rss.indeed.com/rss?q=ag
http://rss.indeed.com/rss?q=ah
http://rss.indeed.com/rss?q=ai
http://rss.indeed.com/rss?q=aj
http://rss.indeed.com/rss?q=ak
http://rss.indeed.com/rss?q=al
http://rss.indeed.com/rss?q=am
http://rss.indeed.com/rss?q=an
http://rss.indeed.com/rss?q=ao
http://rss.indeed.com/rss?q=ap
http://rss.indeed.com/rss?q=aq
http://rss.indeed.com/rss?q=ar
http://rss.indeed.com/rss?q=as   
http://rss.indeed.com/rss?q=at
http://rss.indeed.com/rss?q=au
http://rss.indeed.com/rss?q=av
http://rss.indeed.com/rss?q=aw
http://rss.indeed.com/rss?q=ax
http://rss.indeed.com/rss?q=ay
http://rss.indeed.com/rss?q=az

 
  a b c d e f g h i j k l m n. o p q r s t u v w x y ...
    'http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daz&max=90&links=preserve&exc=&submit=Create+Feed']

# sample URL http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=30&paged=4&submit=Create+Feed&links=preserve

masterletter = "a"
alphabet = ["a","b","c","d","e","f","g"]
pagenum = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

for i in range(len(alphabet)):       

    for p in range(len(pagenum)):

#        source = "http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3D" += masterletter += alphabet[i] "&max=30&paged=" += pagenum[p] += "&submit=Create+Feed&links=preserve"

        source = "http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3Daa&max=30&paged=4&submit=Create+Feed&links=preserve"

        html = scraperwiki.scrape(source)        #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup
        items = soup.findAll('item')             #print type(items) #print items[0]


        article = {}

        for item in items:
            article['title'] = item.find('title').text
            article['url'] = item.find('link').next # wow, this worked!
            article['ingress'] = item.find('description').text
            article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)     
            article['now'] = datetime.now()
            print article
            # the sensfull thing here would be to build a func to scrape the url form here.

        scraperwiki.sqlite.save(['title'], article)
