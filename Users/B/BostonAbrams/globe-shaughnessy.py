import scraperwiki
from bs4 import BeautifulSoup

def getSummary(url):
    storyHtml = scraperwiki.scrape(url)
    storySoup = BeautifulSoup(storyHtml+"?camp=scraper")
    storyMeta = storySoup('meta')
    print storyMeta
    for meta in storyMeta:
        print str(meta).find('name="description"')
        if (str(meta).find('name="description"') > 1):
            summary = str(meta).split('"')[1]
            print summary
            return summary
    return ""

html = scraperwiki.scrape("http://www.bostonglobe.com/staff/shaughnessy")

soup = BeautifulSoup(html)
h3s = soup('h3')
print h3s
for story in h3s[3:9]:
    link = 'http://www.bostonglobe.com'+ story.find('a').get('href')
    description = getSummary(link)
    headline = story.find('a').text
    datestart = link.find('2012')
    datestring= link[datestart:datestart+10] + ' 14:00'
    data = {
      'link' : link,
      'title' : story.find('a').text.strip(), 
      'description': description,
      'pubDate':datestring
    }
    
    print data
    scraperwiki.sqlite.save(unique_keys=['link'], data=data)
