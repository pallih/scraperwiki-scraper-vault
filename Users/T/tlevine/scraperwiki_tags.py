from requests import get
from lxml.html import fromstring
import os

def sgat(level):
    tags = get('https://scraperwiki.com/tags', verify=False).text
    html = fromstring(tags)
    html.make_links_absolute('https://scraperwiki.com/tags')
    links = html.xpath('//ul[@class="cloud tags"]/li/a/@href')
    
    for link in links:
        if level == 'experimental':
            os.system('wget --no-check-certificate %s &' % link)
        elif level == 'control':
            os.system('wget --no-check-certificate %s &' % 'https://scraperwiki.com')

    #    if get('http://hacks.thomaslevine.com/break').status_code == 404:
    #        get(link, verify = False)
    #    else:
    #        break

sgat('experimental')
sgat('control')
from requests import get
from lxml.html import fromstring
import os

def sgat(level):
    tags = get('https://scraperwiki.com/tags', verify=False).text
    html = fromstring(tags)
    html.make_links_absolute('https://scraperwiki.com/tags')
    links = html.xpath('//ul[@class="cloud tags"]/li/a/@href')
    
    for link in links:
        if level == 'experimental':
            os.system('wget --no-check-certificate %s &' % link)
        elif level == 'control':
            os.system('wget --no-check-certificate %s &' % 'https://scraperwiki.com')

    #    if get('http://hacks.thomaslevine.com/break').status_code == 404:
    #        get(link, verify = False)
    #    else:
    #        break

sgat('experimental')
sgat('control')
