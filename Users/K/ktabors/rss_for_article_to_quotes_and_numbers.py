from urllib2 import urlopen
from lxml.html import fromstring, tostring
import re


# common speech verbs in news:
COMMON_VERBS = ['said', 'noted', 'added', 'disagreed', 'pointed out', 'agreed', 'explained', 'according to', 'says','wrote', 'stated', 'declared', 'responded']


RSS_URLS = [
    'http://www.baycitizen.org/feeds/stories/',
    'http://californiawatch.org/feed',
    'http://www.huffingtonpost.com/feeds/verticals/politics/index.xml',
    'http://feeds.nytimes.com/nyt/rss/HomePage'
]

def extract_quotes(text):
    results = []

    for verb in COMMON_VERBS:
        pre_quoted = re.compile(r'([^,.]*) %s[,:]? "([^"]*)[,.?!]"' %verb)
        for value in pre_quoted.findall(text):
            quote = {
                'name': value[0],
                'quote': value[1]
            }
            results.append(quote)

        pre_post_quoted = re.compile(r'"([^"]*)[,.?!]" ([^,.]*) %s[,.]?' %verb)
        for value in pre_post_quoted.findall(text):
            quote = {
                'name': value[1],
                'quote': value[0]
            }
            results.append(quote)

        post_post_quoted = re.compile(r'"([^"]*)[,.?!]" %s ([^,.]*)' %verb)
        for value in post_post_quoted.findall(text):
            quote = {
                'name': value[1],
                'quote': value[0]
            }
            results.append(quote)

    return results
# end def

def rssToArticle(rssURL):
    rss = urlopen(rssURL).read()
    html = fromstring(rss)

    for link in html.cssselect('link'):
        # for some reason tet_content isn't working, but taking the string misus the link tag does
        url = tostring(link)[6:]
        #print url

        # some RSS feeds have the link href as an attribute
        if url[0:7] != "http://":
            continue
        
        article = urlopen(url).read()
        article_html = fromstring(article)
        for p in article_html.cssselect('p'):
            quotes = extract_quotes(p.text_content())
            for quote in quotes:
                print "       " + quote['name'] + " -> " + quote['quote']
# end def

for rssUrl in RSS_URLS:
    #print rssUrl
    rssToArticle(rssUrl)


