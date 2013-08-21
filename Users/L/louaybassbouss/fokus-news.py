#########################################################################################
# scraper for http://www.fokus.fraunhofer.de/en/fokus/news_events/fokus_news/index.html #
#########################################################################################

import scraperwiki
import re
import time
from datetime import datetime
from BeautifulSoup import BeautifulSoup

def scrape_single_news(url, newstype,cc,date,timestamp,image,title):
    html = scraperwiki.scrape(url)
    html = BeautifulSoup(html)
    content_block = html.find('div', {'class': 'contentBlocks'})
    title_elem = content_block.find('h1');
    title = title_elem.text
    title_elem.extract()
    elems = content_block.findAll('table')
    [elem.extract() for elem in elems]
    content = content_block.text
    scraperwiki.sqlite.save(unique_keys=['url'], data={'url':url, 'title':title, 'content': content, 'image': image, 'type': newstype, 'cc': cc, 'date': date, 'timestamp':timestamp})

def run(newstype,url):
    html = scraperwiki.scrape(url)
    html = BeautifulSoup(html)
    news_block = html.find('div', {'id': 'contentRahmen'})
    news_links = news_block.findAll('a', href = re.compile(r"/en/.*?/_.*?news/.*?\.html")) 
    for news_link in news_links:
        title = news_link.text
        image = url.replace('index.html','')+news_link.findPrevious('img')['src']
        date = news_link.findNext('div').text
        timestamp = time.mktime(datetime.strptime(date, "%d.%m.%Y %H:%M").timetuple())
        cc = news_link.findPrevious('hr')['class']
        cc= cc.replace('hr','',1).replace(' ccClear','')
        scrape_single_news('http://www.fokus.fraunhofer.de'+news_link['href'], newstype,cc,date,timestamp,image,title)


sites = {'ARCHIVE': 'http://www.fokus.fraunhofer.de/en/fokus/news_events/fokus_news_archive/index.html',
         'FOKUS': 'http://www.fokus.fraunhofer.de/en/fokus/news_events/fokus_news/index.html',
         'ELAN': 'http://www.fokus.fraunhofer.de/en/elan/index.html',
         'FAME': 'http://www.fokus.fraunhofer.de/en/fame/index.html',
         'NGNI': 'http://www.fokus.fraunhofer.de/en/ngni/index.html',
         'MOTION': 'http://www.fokus.fraunhofer.de/en/motion/index.html',
         'RESCON':'http://www.fokus.fraunhofer.de/en/rescon/index.html',
         'ASCT': 'http://www.fokus.fraunhofer.de/en/asct/index.html'}

for (newstype,url) in sites.items():
    run(newstype,url)
