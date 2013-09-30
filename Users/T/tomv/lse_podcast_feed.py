"""
LSE Podcast scraper
See http://www2.lse.ac.uk/newsAndMedia/videoAndAudio/channels/publicLecturesAndEvents/latest100.aspx
"""

PODCAST_URL = "http://www2.lse.ac.uk/newsAndMedia/videoAndAudio/channels/publicLecturesAndEvents/latest500.aspx?top=9999"

import scraperwiki
import datetime
import requests
from pyquery import PyQuery

try:
    old_mp3s = scraperwiki.sqlite.select("mp3, mp3_bytes from swdata")
except scraperwiki.sqlite.SqliteError, e:
    print repr(e)
    old_mp3s = {}

print len(old_mp3s), 'mp3s found in db'
mp3_bytes = dict((mp3['mp3'], mp3['mp3_bytes']) for mp3 in old_mp3s)


def head(url):
    print 'HEAD', url
    return requests.head(url)

def content_length(url, default='0'):
    return head(url).headers.get('Content-Length', default)

def get_bytes(url, cache=mp3_bytes):
    return cache.get(url, None) or content_length(url)

# Get podcast contents
html = scraperwiki.scrape(PODCAST_URL)
S = PyQuery(html)

episodes = S('.sys_listing_item')

for episode in episodes:
    data = {}
    ep = S(episode)
    data['title'] = ep.find('a').eq(0).text()
    data['link'] = 'http://www2.lse.ac.uk' + ep.find('a').eq(0).attr('href')
    data['mp3'] = ep.find('a:contains("Audio")').eq(0).attr('href')
    data['mp3_bytes'] = get_bytes(data['mp3'])
    data['description'] = ep.text().split('Speaker(s):')[1].split('Play | Download')[0]
    date = ep.text().split('Recorded on:')[1].split('Speaker')[0].strip()
    date = datetime.datetime.strptime(date, '%d %B %Y')
    data['pubdate'] = date.strftime('%a, %d %b %Y %H:%M:%S -0000')
    scraperwiki.sqlite.save(unique_keys=["link"], data=data)
print data
print "Podcast saved!"
"""
LSE Podcast scraper
See http://www2.lse.ac.uk/newsAndMedia/videoAndAudio/channels/publicLecturesAndEvents/latest100.aspx
"""

PODCAST_URL = "http://www2.lse.ac.uk/newsAndMedia/videoAndAudio/channels/publicLecturesAndEvents/latest500.aspx?top=9999"

import scraperwiki
import datetime
import requests
from pyquery import PyQuery

try:
    old_mp3s = scraperwiki.sqlite.select("mp3, mp3_bytes from swdata")
except scraperwiki.sqlite.SqliteError, e:
    print repr(e)
    old_mp3s = {}

print len(old_mp3s), 'mp3s found in db'
mp3_bytes = dict((mp3['mp3'], mp3['mp3_bytes']) for mp3 in old_mp3s)


def head(url):
    print 'HEAD', url
    return requests.head(url)

def content_length(url, default='0'):
    return head(url).headers.get('Content-Length', default)

def get_bytes(url, cache=mp3_bytes):
    return cache.get(url, None) or content_length(url)

# Get podcast contents
html = scraperwiki.scrape(PODCAST_URL)
S = PyQuery(html)

episodes = S('.sys_listing_item')

for episode in episodes:
    data = {}
    ep = S(episode)
    data['title'] = ep.find('a').eq(0).text()
    data['link'] = 'http://www2.lse.ac.uk' + ep.find('a').eq(0).attr('href')
    data['mp3'] = ep.find('a:contains("Audio")').eq(0).attr('href')
    data['mp3_bytes'] = get_bytes(data['mp3'])
    data['description'] = ep.text().split('Speaker(s):')[1].split('Play | Download')[0]
    date = ep.text().split('Recorded on:')[1].split('Speaker')[0].strip()
    date = datetime.datetime.strptime(date, '%d %B %Y')
    data['pubdate'] = date.strftime('%a, %d %b %Y %H:%M:%S -0000')
    scraperwiki.sqlite.save(unique_keys=["link"], data=data)
print data
print "Podcast saved!"
