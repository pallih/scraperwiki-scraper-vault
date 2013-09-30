import scraperwiki, requests, lxml.html, re
from lxml import etree
from time import sleep

# Scraper requested by Tom Ashton on the google group:
# https://groups.google.com/forum/?fromgroups=#!topic/scraperwiki/9FbgYB0ArTs
# Scrapes specified words, their popularities, and pronunciations.
# Sleeps 1 second between requests.
# Database contents are © Macmillan Pulishers Ltd.

# Define your search terms in here, 
# one per line, between the """ marks.
words = """
dream
job
Pass
work
apply
study
study
artificial
sandwich
rice
sandwich
solar
wind
take
alternative
artificial
disease
domestic
genetic
processing
time
voice
science
assembly
carbon
factory
mass
political
production
desalination
endangered
energy
environmental
solar
water
World
protected
bring
carry
come
get
give
keep
put
set
take
take
take
take
try
try
turn
turn
wake
automatic
fossil
global
greenhouse
steering
washing
climate
e-commerce
mock
perfect
physical
"""

word_list = words.strip().splitlines()

data = []

def scrape_details(dom):
    global data
    word = text(dom, '.BASE')
    if word:
        print ':)', word
        data.append({
            'word': word,
            'stars': max(0, len(dom.cssselect('#headword img'))-2),
            'part_of_speech': text(dom, '.PART-OF-SPEECH'),
            'pronunciation_ipa': text(dom, '.PRON', '').replace(u'\xa0', '').encode("UTF-8"),
            'pronunciation_mp3': get_part_of_attr(dom, '.PRONS img', 'onclick', r'http\S+mp3'),
            'definition': text(dom, '.DEFINITION')
        })

def text(dom, selector, not_found=None):
    r = dom.cssselect(selector)
    if len(r):
        return r[0].text_content()
    else:
        return not_found

def get_part_of_attr(dom, selector, attr, regexp):
    r = dom.cssselect(selector)
    if len(r):
        r2 = r[0].get(attr)
        if len(r2):
            matches = re.findall(regexp, r2)
            if len(matches):
                return matches[0]
    return None

try:
    for word in word_list:
        r = requests.get("http://www.macmillandictionary.com/dictionary/british/" + word)
        html = r.text
        dom = lxml.html.fromstring(html)
        if '<h1>Sorry, no search result for' in html:
            if len(dom.cssselect('#search-results li')):
                tophit = dom.cssselect('#search-results li a')[0]
                print ':s multiple entries for:', word
                print '-> disambiguating to:', tophit.text 
                r = requests.get(tophit.get('href'))
                html = r.text
                dom = lxml.html.fromstring(html)
                scrape_details(dom)
            else:
                print '!! no dictionary entry for:', word
        else:
            scrape_details(dom)
        # sleep(0.5)
except:
    print 'saving', len(data), 'records'
    scraperwiki.sqlite.save(['word'], data, 'words')
    raise
else:
    print 'saving', len(data), 'records'
    scraperwiki.sqlite.save(['word'], data, 'words')import scraperwiki, requests, lxml.html, re
from lxml import etree
from time import sleep

# Scraper requested by Tom Ashton on the google group:
# https://groups.google.com/forum/?fromgroups=#!topic/scraperwiki/9FbgYB0ArTs
# Scrapes specified words, their popularities, and pronunciations.
# Sleeps 1 second between requests.
# Database contents are © Macmillan Pulishers Ltd.

# Define your search terms in here, 
# one per line, between the """ marks.
words = """
dream
job
Pass
work
apply
study
study
artificial
sandwich
rice
sandwich
solar
wind
take
alternative
artificial
disease
domestic
genetic
processing
time
voice
science
assembly
carbon
factory
mass
political
production
desalination
endangered
energy
environmental
solar
water
World
protected
bring
carry
come
get
give
keep
put
set
take
take
take
take
try
try
turn
turn
wake
automatic
fossil
global
greenhouse
steering
washing
climate
e-commerce
mock
perfect
physical
"""

word_list = words.strip().splitlines()

data = []

def scrape_details(dom):
    global data
    word = text(dom, '.BASE')
    if word:
        print ':)', word
        data.append({
            'word': word,
            'stars': max(0, len(dom.cssselect('#headword img'))-2),
            'part_of_speech': text(dom, '.PART-OF-SPEECH'),
            'pronunciation_ipa': text(dom, '.PRON', '').replace(u'\xa0', '').encode("UTF-8"),
            'pronunciation_mp3': get_part_of_attr(dom, '.PRONS img', 'onclick', r'http\S+mp3'),
            'definition': text(dom, '.DEFINITION')
        })

def text(dom, selector, not_found=None):
    r = dom.cssselect(selector)
    if len(r):
        return r[0].text_content()
    else:
        return not_found

def get_part_of_attr(dom, selector, attr, regexp):
    r = dom.cssselect(selector)
    if len(r):
        r2 = r[0].get(attr)
        if len(r2):
            matches = re.findall(regexp, r2)
            if len(matches):
                return matches[0]
    return None

try:
    for word in word_list:
        r = requests.get("http://www.macmillandictionary.com/dictionary/british/" + word)
        html = r.text
        dom = lxml.html.fromstring(html)
        if '<h1>Sorry, no search result for' in html:
            if len(dom.cssselect('#search-results li')):
                tophit = dom.cssselect('#search-results li a')[0]
                print ':s multiple entries for:', word
                print '-> disambiguating to:', tophit.text 
                r = requests.get(tophit.get('href'))
                html = r.text
                dom = lxml.html.fromstring(html)
                scrape_details(dom)
            else:
                print '!! no dictionary entry for:', word
        else:
            scrape_details(dom)
        # sleep(0.5)
except:
    print 'saving', len(data), 'records'
    scraperwiki.sqlite.save(['word'], data, 'words')
    raise
else:
    print 'saving', len(data), 'records'
    scraperwiki.sqlite.save(['word'], data, 'words')