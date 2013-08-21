import re
from urllib2 import urlopen
from lxml.html import fromstring, tostring

from scraperwiki.sqlite import save, select, attach

# common speech verbs in news:
COMMON_VERBS = ['said', 'noted', 'added', 'disagreed', 'pointed out', 'agreed', 'explained', 'according to', 'says','wrote', 'stated', 'declared', 'responded']

def extract_quotes(text):
    results = []
    
    for verb in COMMON_VERBS:
        pre_quoted = re.compile(r'([^,.]*) %s[,]? "([^"]*)[,.?!]"' %verb)
        for value in pre_quoted.findall(text):
            quote = {
                'name': value[0],
                'quote': value[1]
            }
            results.append(quote)
            #print "foo"
    
        post_quoted = re.compile(r'"([^"]*)[,.?!]" %s[,]? ([^,.]*)' %verb)
        for value in post_quoted.findall(text):
            quote = {
                'name': value[1],
                'quote': value[0]
            }
            results.append(quote)
            #print "bar"


    all_quotes = re.compile(r'"([^"]*)[,.?!]"')
    for value in all_quotes.findall(text):
        quote = {
            'name': '',
            'quote': value
        }
        #results.append(quote)
        #print "a quote" + value
    return results


print extract_quotes('"yes," declared Alex.')


attach('feedzilla')
articles = select('* from feedzilla.swdata limit 20')
    
for article in articles:
    quotes = extract_quotes(article['text'])
    if not quotes:
        continue
    for quote in quotes:
        record = {
            'url': article['url'],
            'date': article['date'],
            'name': quote['name'],
            'quote': quote['quote']
        }
        print record
        #save([], record)

