# Blank Python
import scraperwiki
import math
import itertools
import string
from nltk.corpus import stopwords



# Hey Nicola,
#
# So, I tested this View on my Mac, and it's fine. No jerky scrolling/shuddering.
# It must be down to your version of Chrome? And all your other Views (without
# the "<!DOCTYPE html>…</html>" bits in) work fine too, which is odd. Anyway, I've
# commented out the stuff we added earlier, since it isn't helping or hindering.
# If you want me to look into what's causing the shuddering on your Mac, just ask.
#
# Zarino :-)
# 2pm 18th Nov 2011




# print "<!DOCTYPE html><html><title>Python Word Cloud</title><head></head><body>"

sourcescraper = 'mailonline_twitter_followers'
scraperwiki.sqlite.attach(sourcescraper, "src")

sdata = scraperwiki.sqlite.execute("SELECT bio FROM src.swdata")
#print sdata['data']
word_list = sdata['data']
big_list = list(itertools.chain(*word_list))
#print big_list
big_list= [x for x in big_list if x is not None]

#print big_list

thestopwords = [x for x in stopwords.words('english')]
#print thestopwords

spanish_words = ['en', 'de', 'y', 'la', 'e']
words = {}
for sentence in big_list:
    for word in sentence.split(' '):
        w = word.strip(string.punctuation + string.whitespace).lower()
        if w and w not in thestopwords:
            words[w] = words.get(w, 0) + 1

for word in spanish_words:
    if word in words:
        del words[word]

for k,v in words.iteritems():
    if v > 280:
        print "<span style='font-size:%dpx;'>%s  </span>" % (v/10,k,)


# print "<span style='clear:left; display:block'></span></body></html>"
# Blank Python
import scraperwiki
import math
import itertools
import string
from nltk.corpus import stopwords



# Hey Nicola,
#
# So, I tested this View on my Mac, and it's fine. No jerky scrolling/shuddering.
# It must be down to your version of Chrome? And all your other Views (without
# the "<!DOCTYPE html>…</html>" bits in) work fine too, which is odd. Anyway, I've
# commented out the stuff we added earlier, since it isn't helping or hindering.
# If you want me to look into what's causing the shuddering on your Mac, just ask.
#
# Zarino :-)
# 2pm 18th Nov 2011




# print "<!DOCTYPE html><html><title>Python Word Cloud</title><head></head><body>"

sourcescraper = 'mailonline_twitter_followers'
scraperwiki.sqlite.attach(sourcescraper, "src")

sdata = scraperwiki.sqlite.execute("SELECT bio FROM src.swdata")
#print sdata['data']
word_list = sdata['data']
big_list = list(itertools.chain(*word_list))
#print big_list
big_list= [x for x in big_list if x is not None]

#print big_list

thestopwords = [x for x in stopwords.words('english')]
#print thestopwords

spanish_words = ['en', 'de', 'y', 'la', 'e']
words = {}
for sentence in big_list:
    for word in sentence.split(' '):
        w = word.strip(string.punctuation + string.whitespace).lower()
        if w and w not in thestopwords:
            words[w] = words.get(w, 0) + 1

for word in spanish_words:
    if word in words:
        del words[word]

for k,v in words.iteritems():
    if v > 280:
        print "<span style='font-size:%dpx;'>%s  </span>" % (v/10,k,)


# print "<span style='clear:left; display:block'></span></body></html>"
