import scraperwiki
from collections import Counter, defaultdict

# scrape the gdoc of all the words (already cleaned of punctuation)
stories = scraperwiki.scrape('https://docs.google.com/document/pub?id=10psphQjuxB_apQLxZBSkuk934-q6YjZoKFiz5nSeNdA')

print stories

#split the scraped page at every space (default option - put something in parentheses to specify other)
#and put results in a list
storieswords = stories.split()

print storieswords

#the following is taken from http://stackoverflow.com/questions/4088265/word-frequency-count-using-python

#use Counter function to count occurrences of words and put result in wordfreq (a dict)
wordfreq = Counter(storieswords)

print wordfreq

#use defaultdict to create a new empty object called freqword
freqword = defaultdict(list)
#loop through items in wordfreq and for each one append to freqword under 'freq'
for word, freq in wordfreq.items():
    freqword[freq].append(word)

print freqword

# print in order of occurrence
occurrences = freqword.keys()
occurrences.sort()
ID = 0
for freq in occurrences:
    freqword[freq].sort() # sort words in list
    print 'count {}: {}'.format(freq, freqword[freq])
    record = {}
    record['count'] = 'count {}: {}'.format(freq, freqword[freq])
#    record['ID'] = ID =+ 1
    print record, '------------'
    scraperwiki.datastore.save(["count"], record)
import scraperwiki
from collections import Counter, defaultdict

# scrape the gdoc of all the words (already cleaned of punctuation)
stories = scraperwiki.scrape('https://docs.google.com/document/pub?id=10psphQjuxB_apQLxZBSkuk934-q6YjZoKFiz5nSeNdA')

print stories

#split the scraped page at every space (default option - put something in parentheses to specify other)
#and put results in a list
storieswords = stories.split()

print storieswords

#the following is taken from http://stackoverflow.com/questions/4088265/word-frequency-count-using-python

#use Counter function to count occurrences of words and put result in wordfreq (a dict)
wordfreq = Counter(storieswords)

print wordfreq

#use defaultdict to create a new empty object called freqword
freqword = defaultdict(list)
#loop through items in wordfreq and for each one append to freqword under 'freq'
for word, freq in wordfreq.items():
    freqword[freq].append(word)

print freqword

# print in order of occurrence
occurrences = freqword.keys()
occurrences.sort()
ID = 0
for freq in occurrences:
    freqword[freq].sort() # sort words in list
    print 'count {}: {}'.format(freq, freqword[freq])
    record = {}
    record['count'] = 'count {}: {}'.format(freq, freqword[freq])
#    record['ID'] = ID =+ 1
    print record, '------------'
    scraperwiki.datastore.save(["count"], record)
import scraperwiki
from collections import Counter, defaultdict

# scrape the gdoc of all the words (already cleaned of punctuation)
stories = scraperwiki.scrape('https://docs.google.com/document/pub?id=10psphQjuxB_apQLxZBSkuk934-q6YjZoKFiz5nSeNdA')

print stories

#split the scraped page at every space (default option - put something in parentheses to specify other)
#and put results in a list
storieswords = stories.split()

print storieswords

#the following is taken from http://stackoverflow.com/questions/4088265/word-frequency-count-using-python

#use Counter function to count occurrences of words and put result in wordfreq (a dict)
wordfreq = Counter(storieswords)

print wordfreq

#use defaultdict to create a new empty object called freqword
freqword = defaultdict(list)
#loop through items in wordfreq and for each one append to freqword under 'freq'
for word, freq in wordfreq.items():
    freqword[freq].append(word)

print freqword

# print in order of occurrence
occurrences = freqword.keys()
occurrences.sort()
ID = 0
for freq in occurrences:
    freqword[freq].sort() # sort words in list
    print 'count {}: {}'.format(freq, freqword[freq])
    record = {}
    record['count'] = 'count {}: {}'.format(freq, freqword[freq])
#    record['ID'] = ID =+ 1
    print record, '------------'
    scraperwiki.datastore.save(["count"], record)
