from urllib2 import urlparse

import scraperwiki
import lxml.html
import datetime

BASE = 'http://game-quotes.com/de'
LIST = '/glist.php'

def parse_page(url):
    root = lxml.html.parse(url).getroot()
    global id
    id = 0
    for row in root.cssselect('.fliste2 a, a.glist'):
        print row.text
        parse_game(row.attrib['href'], row.text)        

def parse_game(url, gameName):
    try:
        print url
        gameroot = lxml.html.parse(url).getroot()
    except:
        gameroot = lxml.html.parse('http://game-quotes.com/de/' + url).getroot()
    global id
    for row in gameroot.cssselect('li.zlist'):
        print row.text
        qoute = {}
        qoute["game"] = gameName
        qoute["qoute"] = row.text
        qoute["id"] = id
        scraperwiki.sqlite.save(unique_keys=["id"], data=qoute)
        id += 1

def main():
    parse_page(BASE+LIST)

main()
from urllib2 import urlparse

import scraperwiki
import lxml.html
import datetime

BASE = 'http://game-quotes.com/de'
LIST = '/glist.php'

def parse_page(url):
    root = lxml.html.parse(url).getroot()
    global id
    id = 0
    for row in root.cssselect('.fliste2 a, a.glist'):
        print row.text
        parse_game(row.attrib['href'], row.text)        

def parse_game(url, gameName):
    try:
        print url
        gameroot = lxml.html.parse(url).getroot()
    except:
        gameroot = lxml.html.parse('http://game-quotes.com/de/' + url).getroot()
    global id
    for row in gameroot.cssselect('li.zlist'):
        print row.text
        qoute = {}
        qoute["game"] = gameName
        qoute["qoute"] = row.text
        qoute["id"] = id
        scraperwiki.sqlite.save(unique_keys=["id"], data=qoute)
        id += 1

def main():
    parse_page(BASE+LIST)

main()
