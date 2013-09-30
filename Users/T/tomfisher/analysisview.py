# Blank Python
from nltk import *
import numpy
import matplotlib
#import nltk
sourcescraper = 'eg-analyseposts'
import scraperwiki
scraperwiki.sqlite.attach("eg-analyseposts", "src")

ueberstringdb = scraperwiki.sqlite.select("* from allinone limit 10")
separatepostsdb = scraperwiki.sqlite.select("* from swdata limit 10")

#print test
#print type(test)
#print type(test[0])
#print type(test[0].values())


print type(ueberstringdb)
print len(ueberstringdb)
ueberdb = ueberstringdb[0]
print type(ueberdb)
ueberstring = ueberdb['ueber']
"""
def txt_to_nltk(filename):
    raw = filename
    tokens = word_tokenize(raw)
    words = [w.lower() for w in tokens]
    vocab = sorted(set(words))
    cleaner_tokens = wordpunct_tokenize(raw)
    # "Text" is a datatype in NLTK
    tweets = Text(tokens)
    # For language nerds, you can tag the Parts of Speech!
    tagged = pos_tag(cleaner_tokens)
    return dict(
                raw = raw,
                tokens = tokens,
                words = words,
                vocab = vocab,
                cleaner_tokens = cleaner_tokens,
                tweets = tweets,
                tagged = tagged
                )
""" 
#superstring = txt_to_nltk(ueberstring)



#ueberstring.concordance("capita")

uebertext = Text(ueberstring)
uebertext.dispersion_plot(["sims", "capita", "council", "school"])


#print ueberstring

#for row in ueberstringdb:
#    print row['ueber']
#print ueberstringdb['ueber']


#the below two lines ACTually create an ueberstring
#templist = ueberstringdb[0].values()
#ueberstring = templist[0]
#print ueberstring[ueber]

"""

print type(separatepostsdb)

for postsitem in separatepostsdb:
    #print type(postsitem)
    #print postsitem.keys()
    datestring = postsitem[u'date']
    pds = datestring.split()
    print pds[0]
    print pds[0].replace(' ', '')[:-2].upper()
"""

    
# Blank Python
from nltk import *
import numpy
import matplotlib
#import nltk
sourcescraper = 'eg-analyseposts'
import scraperwiki
scraperwiki.sqlite.attach("eg-analyseposts", "src")

ueberstringdb = scraperwiki.sqlite.select("* from allinone limit 10")
separatepostsdb = scraperwiki.sqlite.select("* from swdata limit 10")

#print test
#print type(test)
#print type(test[0])
#print type(test[0].values())


print type(ueberstringdb)
print len(ueberstringdb)
ueberdb = ueberstringdb[0]
print type(ueberdb)
ueberstring = ueberdb['ueber']
"""
def txt_to_nltk(filename):
    raw = filename
    tokens = word_tokenize(raw)
    words = [w.lower() for w in tokens]
    vocab = sorted(set(words))
    cleaner_tokens = wordpunct_tokenize(raw)
    # "Text" is a datatype in NLTK
    tweets = Text(tokens)
    # For language nerds, you can tag the Parts of Speech!
    tagged = pos_tag(cleaner_tokens)
    return dict(
                raw = raw,
                tokens = tokens,
                words = words,
                vocab = vocab,
                cleaner_tokens = cleaner_tokens,
                tweets = tweets,
                tagged = tagged
                )
""" 
#superstring = txt_to_nltk(ueberstring)



#ueberstring.concordance("capita")

uebertext = Text(ueberstring)
uebertext.dispersion_plot(["sims", "capita", "council", "school"])


#print ueberstring

#for row in ueberstringdb:
#    print row['ueber']
#print ueberstringdb['ueber']


#the below two lines ACTually create an ueberstring
#templist = ueberstringdb[0].values()
#ueberstring = templist[0]
#print ueberstring[ueber]

"""

print type(separatepostsdb)

for postsitem in separatepostsdb:
    #print type(postsitem)
    #print postsitem.keys()
    datestring = postsitem[u'date']
    pds = datestring.split()
    print pds[0]
    print pds[0].replace(' ', '')[:-2].upper()
"""

    
