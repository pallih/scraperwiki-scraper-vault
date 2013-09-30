#coding: utf-8
import scraperwiki
from BeautifulSoup import BeautifulSoup, NavigableString, Declaration, Comment
import datetime
import urllib

URL = "http://www.moe-chan.com/moe-sys/index.php"
html = scraperwiki.scrape(URL)


soup = BeautifulSoup(html)

for name_and_time in soup.findAll('div',{'class':'photos'}):
    name = name_and_time.find('a')
    time = name_and_time.find('span',{'class':'tc'})

    if name != None:
        if time != None:
           zyou = {}
           zyou['name'] = str([e for e in name.recursiveChildGenerator() if isinstance(e,unicode)][0])
           zyou['work_time_end'], zyou['work_time_start'] \
                = [t for t in [e for e in time.recursiveChildGenerator() if isinstance(e,unicode)][0].split(u'〜')]
           scraperwiki.sqlite.save(['name', 'work_time_start', 'work_time_end'], zyou)

#coding: utf-8
import scraperwiki
from BeautifulSoup import BeautifulSoup, NavigableString, Declaration, Comment
import datetime
import urllib

URL = "http://www.moe-chan.com/moe-sys/index.php"
html = scraperwiki.scrape(URL)


soup = BeautifulSoup(html)

for name_and_time in soup.findAll('div',{'class':'photos'}):
    name = name_and_time.find('a')
    time = name_and_time.find('span',{'class':'tc'})

    if name != None:
        if time != None:
           zyou = {}
           zyou['name'] = str([e for e in name.recursiveChildGenerator() if isinstance(e,unicode)][0])
           zyou['work_time_end'], zyou['work_time_start'] \
                = [t for t in [e for e in time.recursiveChildGenerator() if isinstance(e,unicode)][0].split(u'〜')]
           scraperwiki.sqlite.save(['name', 'work_time_start', 'work_time_end'], zyou)

