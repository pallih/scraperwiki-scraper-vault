import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

url = "https://spreadsheets.google.com/feeds/list/0Aqe_ujdJk_IPdDc4Wkh0RzNGR29VNVFIQWRVS2hybVE/od4/public/basic?hl=en_US&alt=rss"

data = urllib.urlopen(url).read()
root = lxml.etree.fromstring(data)

for channel in root:
    for item in channel:
        for elem in item:
            if elem.tag == 'description':
                blob = re.match('(?s)<description.*?>(.*?)</description>', lxml.etree.tostring(elem)).group(1)
                title = re.search('title', blob).group()
                print title
import scraperwiki
import urllib
import lxml.etree, lxml.html
import re

url = "https://spreadsheets.google.com/feeds/list/0Aqe_ujdJk_IPdDc4Wkh0RzNGR29VNVFIQWRVS2hybVE/od4/public/basic?hl=en_US&alt=rss"

data = urllib.urlopen(url).read()
root = lxml.etree.fromstring(data)

for channel in root:
    for item in channel:
        for elem in item:
            if elem.tag == 'description':
                blob = re.match('(?s)<description.*?>(.*?)</description>', lxml.etree.tostring(elem)).group(1)
                title = re.search('title', blob).group()
                print title
