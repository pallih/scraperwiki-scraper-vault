import scraperwiki
import requests
import urllib
import feedparser
import sys
import dateutil.parser
from BeautifulSoup import BeautifulSoup
import time
import random

terms_a = ['Conservation Fund',
        'Conservation International',
        'Environmental Defence Funds',
        'Nature Conservancy', 'TNC',
        'Natural Resources Defense Council', 'NRDC',
        'World Wildlife Fund', 'WWF',
        'Sierra Club',
        'Center for Conservation Biology',
]
terms_b = [ 'BP', 
    # Oil
    'Chevron',
    'Texaco',
    'ConocoPhilips',
    'ExxonMobil',
    'Shell Oil',
    # Power
    'AES',
    'Alliant',
    'American Electric Power', 'AEP',
    'CONSOL',
    'Duke Energy',
    'Entergy',
    'Exelon',
    'Georgia Power',
    'NRG Energy',
    'PG&E',
    'PNM Resources',
    'USX',
    'Chesapeake Energy'
    # Mining
    'Alcoa',
    'Anglo American',
    'BHP Billiton',
    'Rio Tinto',
    # Construction 
    'Bechtel',
    'Cemex',
    'Centex',
    'Home Depot',
    'Ikea',
    "Lowe's",
    'Pulte Homes',
    # Paper & Pulp & logging
    'American Forest & Paper', 'AFPA',
    'Consolidated Paper',
    'Domtar',
    'Georgia-Pacific',
    'International Paper',
    'MeadWestvaco', 'MWV',
    'Plumb Creek Timber',
    'Temple-Inland',
    'Weyerhaeuser',
    # Cruise ship
    'Cruise Lines International',
    'Royal Caribbean Cruises',
    # Chemicals
    'American Chemistry Council',
    'Dow Chemical',
    'DuPont',
    # Agrib-business
    'Bunge',
    'Cargill',
    'Monsanto',
    # Financial services
    'American Express',
    'Bank of America',
    'Banco Nacional',
    'JPMorgan Chase',
    'Citicorp',
    'Citigroup',
    'Goldman Sachs',
    'HSBC',
    'Merrill Lynch',
    'Visa',
    # Food & Beverages
    'Starbucks',
    'Anheuser-Busch',
    'Coca Cola',
    'Coors Brewing',
    'Fiji water',
    "McDonald's",
    "Nestle",
    "PepsiCo",
    # Auto
    'Chrysler',
    'Ford Motor',
    'General Motors',
    'GITI Group',
    'Nissan',
    'Toyota',
    # Retail
    'Gap Inc',
    'Levi Strauss',
    'Amazon.com',
    'Office Depot',
    'Tiffany & Co',
    'Wal-Mart',
    # Consumer goods manufacturing
    'Eastman Kodak',
    'General Electric',
    'General Mills',
    'Johnson & Johnson',
    'Procter & Gamble',
    'SC Johnson & Son',
    'Uniliver',
    # Other
    'Alcan',
    'Boston Scientific',
    'Caterpillar',
    'Deere',
    'Lockheed Martin',
    'Northrop Grumman',
    ]

def get_rss(a, b):
    #alcoa%20AND%20%22sierra%20club%22
    q = '"%s" AND "%s"' % (a, b)
    #url = "http://news.google.com/news?q=%s&output=rss" % urllib.quote(q)
    url = "http://news.search.yahoo.com/rss?ei=UTF-8&p=%s&fr=ush-globalnews&sort=time" % urllib.quote(q)
    print "get url", url
    feed = feedparser.parse(url)
    print "status", feed.status
    if feed.status == 999:
        raise Exception("Yahoo error 999, probably rate limit exceeded: http://www.murraymoffatt.com/software-problem-0011.html")
    if feed.status >= 400:
        raise Exception("Status error querying Yahoo News RSS: " + str(feed.status))
    #print feed['items'][0]
    for item in feed['items']:
        d = { 'updated': dateutil.parser.parse(item['updated']),
              'title': item['title'],
              'summary_html': item['summary'],
              'summary_text': ''.join(BeautifulSoup(item['summary']).findAll(text=True)),
              'link': item['link'],
              'id': item['id'],
              'term_a': a,
              'term_b': b
            }
        scraperwiki.sqlite.save(['link'], d)

print "Terms: %d * %d = %d" % (len(terms_a), len(terms_b), len(terms_a) * len(terms_b))
random.shuffle(terms_a)
random.shuffle(terms_b)
for a in terms_a:
    for b in terms_b:
        get_rss(a,b)
        # sleep for random 0 to 8 seconds to not annoy Yahoo too much
        time.sleep(random.random() * 8)


import scraperwiki
import requests
import urllib
import feedparser
import sys
import dateutil.parser
from BeautifulSoup import BeautifulSoup
import time
import random

terms_a = ['Conservation Fund',
        'Conservation International',
        'Environmental Defence Funds',
        'Nature Conservancy', 'TNC',
        'Natural Resources Defense Council', 'NRDC',
        'World Wildlife Fund', 'WWF',
        'Sierra Club',
        'Center for Conservation Biology',
]
terms_b = [ 'BP', 
    # Oil
    'Chevron',
    'Texaco',
    'ConocoPhilips',
    'ExxonMobil',
    'Shell Oil',
    # Power
    'AES',
    'Alliant',
    'American Electric Power', 'AEP',
    'CONSOL',
    'Duke Energy',
    'Entergy',
    'Exelon',
    'Georgia Power',
    'NRG Energy',
    'PG&E',
    'PNM Resources',
    'USX',
    'Chesapeake Energy'
    # Mining
    'Alcoa',
    'Anglo American',
    'BHP Billiton',
    'Rio Tinto',
    # Construction 
    'Bechtel',
    'Cemex',
    'Centex',
    'Home Depot',
    'Ikea',
    "Lowe's",
    'Pulte Homes',
    # Paper & Pulp & logging
    'American Forest & Paper', 'AFPA',
    'Consolidated Paper',
    'Domtar',
    'Georgia-Pacific',
    'International Paper',
    'MeadWestvaco', 'MWV',
    'Plumb Creek Timber',
    'Temple-Inland',
    'Weyerhaeuser',
    # Cruise ship
    'Cruise Lines International',
    'Royal Caribbean Cruises',
    # Chemicals
    'American Chemistry Council',
    'Dow Chemical',
    'DuPont',
    # Agrib-business
    'Bunge',
    'Cargill',
    'Monsanto',
    # Financial services
    'American Express',
    'Bank of America',
    'Banco Nacional',
    'JPMorgan Chase',
    'Citicorp',
    'Citigroup',
    'Goldman Sachs',
    'HSBC',
    'Merrill Lynch',
    'Visa',
    # Food & Beverages
    'Starbucks',
    'Anheuser-Busch',
    'Coca Cola',
    'Coors Brewing',
    'Fiji water',
    "McDonald's",
    "Nestle",
    "PepsiCo",
    # Auto
    'Chrysler',
    'Ford Motor',
    'General Motors',
    'GITI Group',
    'Nissan',
    'Toyota',
    # Retail
    'Gap Inc',
    'Levi Strauss',
    'Amazon.com',
    'Office Depot',
    'Tiffany & Co',
    'Wal-Mart',
    # Consumer goods manufacturing
    'Eastman Kodak',
    'General Electric',
    'General Mills',
    'Johnson & Johnson',
    'Procter & Gamble',
    'SC Johnson & Son',
    'Uniliver',
    # Other
    'Alcan',
    'Boston Scientific',
    'Caterpillar',
    'Deere',
    'Lockheed Martin',
    'Northrop Grumman',
    ]

def get_rss(a, b):
    #alcoa%20AND%20%22sierra%20club%22
    q = '"%s" AND "%s"' % (a, b)
    #url = "http://news.google.com/news?q=%s&output=rss" % urllib.quote(q)
    url = "http://news.search.yahoo.com/rss?ei=UTF-8&p=%s&fr=ush-globalnews&sort=time" % urllib.quote(q)
    print "get url", url
    feed = feedparser.parse(url)
    print "status", feed.status
    if feed.status == 999:
        raise Exception("Yahoo error 999, probably rate limit exceeded: http://www.murraymoffatt.com/software-problem-0011.html")
    if feed.status >= 400:
        raise Exception("Status error querying Yahoo News RSS: " + str(feed.status))
    #print feed['items'][0]
    for item in feed['items']:
        d = { 'updated': dateutil.parser.parse(item['updated']),
              'title': item['title'],
              'summary_html': item['summary'],
              'summary_text': ''.join(BeautifulSoup(item['summary']).findAll(text=True)),
              'link': item['link'],
              'id': item['id'],
              'term_a': a,
              'term_b': b
            }
        scraperwiki.sqlite.save(['link'], d)

print "Terms: %d * %d = %d" % (len(terms_a), len(terms_b), len(terms_a) * len(terms_b))
random.shuffle(terms_a)
random.shuffle(terms_b)
for a in terms_a:
    for b in terms_b:
        get_rss(a,b)
        # sleep for random 0 to 8 seconds to not annoy Yahoo too much
        time.sleep(random.random() * 8)


