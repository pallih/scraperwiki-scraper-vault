import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime
import re

scraperwiki.sqlite.execute('DELETE FROM swdata')


def stripTags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


masterletter = "r"
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
pagenum = 8

checkAgainst = ['']

dupes=0
totalRecords=0

for index in range(len(alphabet)):       

    for p in xrange(pagenum):

        #print(index,alphabet[index],'',p,str(p))        
        
        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3D", masterletter, alphabet[index], "&max=100&paged=", str(p), "&submit=Create+Feed&links=preserve"]

        source = "".join(sourcearray)


        html = scraperwiki.scrape(source)                                       #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup                                                     
        items = soup.findAll('item')                                            #print type(items) #print items[0]

        article = {}          
        now = {}

        check=0

        for item in items:
            now = item.find('title').text

            article['title'] = stripTags(item.find('title').text)
            #article['title'] = re.sub(r'\[|\]|\s*<[^>]*>\s*', ' ', article['title'])

            article['url'] = item.find('link').next      
              
            article['description'] = stripTags(item.find('description').text)
            #article['description'] = re.sub(r'\[|\]|\s*<[^>]*>\s*', ' ', article['description'])

            article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)   
            article['now'] = datetime.now()        
            print article         
            
            #check against all elems in checkAgainst, if match then escape loop, if unique then proceed
            check==0
            for i in checkAgainst:
                if article['description'] in checkAgainst:
                    check+=1
            
            if check==0:
                #remove first elem in checkAgainst
                if len(checkAgainst)<250:
                    checkAgainst.pop
                #add to bottom of checkAgainst
                checkAgainst.append(article['description'])
                #save to db
                scraperwiki.sqlite.save(['now'], article)
                totalRecords+=1
            else:
                dupes+=1
                print('Duplicates:', dupes, 'Uniques:',totalRecords)



import scraperwiki
from BeautifulSoup import BeautifulSoup
import dateutil.parser
from datetime import datetime
import re

scraperwiki.sqlite.execute('DELETE FROM swdata')


def stripTags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


masterletter = "r"
alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
pagenum = 8

checkAgainst = ['']

dupes=0
totalRecords=0

for index in range(len(alphabet)):       

    for p in xrange(pagenum):

        #print(index,alphabet[index],'',p,str(p))        
        
        sourcearray = ["http://www.jobgymn.com/makefulltextfeed.php?url=rss.indeed.com%2Frss%3Fq%3D", masterletter, alphabet[index], "&max=100&paged=", str(p), "&submit=Create+Feed&links=preserve"]

        source = "".join(sourcearray)


        html = scraperwiki.scrape(source)                                       #print html
        soup = BeautifulSoup(html, convertEntities=BeautifulSoup.HTML_ENTITIES) #print soup                                                     
        items = soup.findAll('item')                                            #print type(items) #print items[0]

        article = {}          
        now = {}

        check=0

        for item in items:
            now = item.find('title').text

            article['title'] = stripTags(item.find('title').text)
            #article['title'] = re.sub(r'\[|\]|\s*<[^>]*>\s*', ' ', article['title'])

            article['url'] = item.find('link').next      
              
            article['description'] = stripTags(item.find('description').text)
            #article['description'] = re.sub(r'\[|\]|\s*<[^>]*>\s*', ' ', article['description'])

            article['pubdate'] = dateutil.parser.parse(item.find('pubdate').text)   
            article['now'] = datetime.now()        
            print article         
            
            #check against all elems in checkAgainst, if match then escape loop, if unique then proceed
            check==0
            for i in checkAgainst:
                if article['description'] in checkAgainst:
                    check+=1
            
            if check==0:
                #remove first elem in checkAgainst
                if len(checkAgainst)<250:
                    checkAgainst.pop
                #add to bottom of checkAgainst
                checkAgainst.append(article['description'])
                #save to db
                scraperwiki.sqlite.save(['now'], article)
                totalRecords+=1
            else:
                dupes+=1
                print('Duplicates:', dupes, 'Uniques:',totalRecords)



