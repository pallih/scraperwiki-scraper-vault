import scraperwiki
from bs4 import BeautifulSoup

def getLength(url):
    try:
        storyHtml = scraperwiki.scrape('http://www.bostonglobe.com'+url)
        storySoup = BeautifulSoup(storyHtml)
        storyContent = storySoup('content')
        print storyContent[1]
        paragraphs = str(storyContent[1]).count('<p')
        print paragraphs
        return paragraphs
    except:
        return 0




def getPaper(day):
    html = scraperwiki.scrape("http://www.bostonglobe.com/todayspaper/2013/06/0"+str(day))
    soup = BeautifulSoup(html)
    links = soup('a')
    print links
    for story in links:
        z  = story.get('href')
        if z.find('2013/06/0'+str(day-1))>1 or z.find('2013/06/0'+str(day)) > 1:
            print 'Yes: '+z
            length = getLength(z)
            data = {
                  'link' : z,
                  'length' : length
                }
            print data
            scraperwiki.sqlite.save(unique_keys=['link'], data=data)
        else:
            print 'No: '+z

print getLength('/metro/2013/04/28/bombreconstruct/VbSZhzHm35yR88EVmVdbDM/story.html')

for i in range(2,8):
    print i
    #getPaper(i)
import scraperwiki
from bs4 import BeautifulSoup

def getLength(url):
    try:
        storyHtml = scraperwiki.scrape('http://www.bostonglobe.com'+url)
        storySoup = BeautifulSoup(storyHtml)
        storyContent = storySoup('content')
        print storyContent[1]
        paragraphs = str(storyContent[1]).count('<p')
        print paragraphs
        return paragraphs
    except:
        return 0




def getPaper(day):
    html = scraperwiki.scrape("http://www.bostonglobe.com/todayspaper/2013/06/0"+str(day))
    soup = BeautifulSoup(html)
    links = soup('a')
    print links
    for story in links:
        z  = story.get('href')
        if z.find('2013/06/0'+str(day-1))>1 or z.find('2013/06/0'+str(day)) > 1:
            print 'Yes: '+z
            length = getLength(z)
            data = {
                  'link' : z,
                  'length' : length
                }
            print data
            scraperwiki.sqlite.save(unique_keys=['link'], data=data)
        else:
            print 'No: '+z

print getLength('/metro/2013/04/28/bombreconstruct/VbSZhzHm35yR88EVmVdbDM/story.html')

for i in range(2,8):
    print i
    #getPaper(i)
