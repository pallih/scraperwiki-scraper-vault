# Blank Python
sourcescraper = 'basic_twitter_scraper_167'
import scraperwiki
import math
import itertools
import string
from nltk.corpus import stopwords


sourcescraper = 'basic_twitter_scraper_167'
scraperwiki.sqlite.attach(sourcescraper, "src")

sdata = scraperwiki.sqlite.execute("SELECT text FROM src.swdata")
#print sdata['data']
word_list = sdata['data']
big_list = list(itertools.chain(*word_list))
#print big_list
big_list= [x for x in big_list if x is not None]

#print big_list

thestopwords = [x for x in stopwords.words('english')]
#print thestopwords

common_twitter = ['rt','oh']
words = {}
for sentence in big_list:
    for word in sentence.split(' '):
        w = word.strip(string.punctuation + string.whitespace).lower()
        if w and w not in thestopwords:
            words[w] = words.get(w, 0) + 1

for word in common_twitter:
    if word in words:
        del words[word]

for k,v in words.iteritems():
    if v > 8:
        print "<span style='font-size:%dpx'>%s</span>" % (v,k,)


# Blank Python
sourcescraper = 'basic_twitter_scraper_167'
import scraperwiki
import math
import itertools
import string
from nltk.corpus import stopwords


sourcescraper = 'basic_twitter_scraper_167'
scraperwiki.sqlite.attach(sourcescraper, "src")

sdata = scraperwiki.sqlite.execute("SELECT text FROM src.swdata")
#print sdata['data']
word_list = sdata['data']
big_list = list(itertools.chain(*word_list))
#print big_list
big_list= [x for x in big_list if x is not None]

#print big_list

thestopwords = [x for x in stopwords.words('english')]
#print thestopwords

common_twitter = ['rt','oh']
words = {}
for sentence in big_list:
    for word in sentence.split(' '):
        w = word.strip(string.punctuation + string.whitespace).lower()
        if w and w not in thestopwords:
            words[w] = words.get(w, 0) + 1

for word in common_twitter:
    if word in words:
        del words[word]

for k,v in words.iteritems():
    if v > 8:
        print "<span style='font-size:%dpx'>%s</span>" % (v,k,)


