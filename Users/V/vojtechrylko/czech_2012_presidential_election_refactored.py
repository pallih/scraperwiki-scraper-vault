import scraperwiki
import simplejson
import urllib2
import unicodedata
import nltk
import string
from collections import Counter
import unicodedata

# which phrases to search (joined by OR)
phrases = [
    '#volbaprezidenta',
    'bobošíková',
    'Dientsbier',
    'Schwarzenberg',
    'miloš zeman',
    '#fisher',
    'Fischerová',
    'Přemysl Sobotka',
    'Vladimír Franz',
    'Roithová',
    'jan Fischer',
    'Vladimír Dlouhý',
    'Okamura',
    '#volby'
]

# stop words
cz_stop = [u'a', u'aby', u'aj', u'ale', u'anebo', u'ani', u'aniz', u'ano', u'asi', u'avska', u'az', u'ba', u'bez', u'bude', u'budem', u'budes', u'by', u'byl', u'byla', u'byli', u'bylo', u'byt', u'ci', u'clanek', u'clanku', u'clanky', u'co', u'com', u'coz', u'cz', u'dalsi', u'design', u'dnes', u'do', u'email', u'ho', u'i', u'jak', u'jake', u'jako', u'je', u'jeho', u'jej', u'jeji', u'jejich', u'jen', u'jeste', u'jenz', u'ji', u'jine', u'jiz', u'jsem', u'jses', u'jsi', u'jsme', u'jsou', u'jste', u'k', u'kam', u'kde', u'kdo', u'kdyz', u'ke', u'ktera', u'ktere', u'kteri', u'kterou', u'ktery', u'ku', u'ma', u'mate', u'me', u'mezi', u'mi', u'mit', u'mne', u'mnou', u'muj', u'muze', u'my', u'na', u'nad', u'nam', u'napiste', u'nas', u'nasi', u'ne', u'nebo', u'nebot', u'necht', u'nejsou', u'není', u'neni', u'net', u'nez', u'ni', u'nic', u'nove', u'novy', u'nybrz', u'o', u'od', u'ode', u'on', u'org', u'pak', u'po', u'pod', u'podle', u'pokud', u'pouze', u'prave', u'pred', u'pres', u'pri', u'pro', u'proc', u'proto', u'protoze', u'prvni', u'pta', u're', u's', u'se', u'si', u'sice', u'spol', u'strana', u'sve', u'svuj', u'svych', u'svym', u'svymi', u'ta', u'tak', u'take', u'takze', u'tamhle', u'tato', u'tedy', u'tema', u'te', u'ten', u'tedy', u'tento', u'teto', u'tim u', u'timto', u'tipy', u'to', u'tohle', u'toho', u'tohoto', u'tom', u'tomto', u'tomuto', u'totiz', u'tu', u'tudiz', u'tuto', u'tvuj', u'ty', u'tyto', u'u', u'uz', u'v', u'vam', u'vas', u'vas', u'vase', u've', u'vedle', u'vice', u'vsak', u'vsechen', u'vy', u'vzdyt', u'z', u'za', u'zda', u'zde', u'ze', u'zpet', u'zpravy']
cz_stop.extend(list(u',./!#@)(}{|"-+*/:'))



RESULTS_PER_PAGE = '500'
NUM_PAGES = 1

class Corpus:
    def __init__(self, stop_words, min_length=0, accents=False):
        self._counter = Counter()
        self._stop_words = filter(lambda a: len(a) >= min_length, stop_words)
        self._min_length = min_length
        self._accents = accents
        self._tokenizer = nltk.tokenize.RegexpTokenizer(r'\S+')

    def add_document(self, text):
        words = self._tokenize(text)
        filtered_words = self._filter_words(words)
        for word in filtered_words:
            self._counter[word] += 1

    def get_counts(self):
         return self._counter 

    def _tokenize(self, in_text):
        text = in_text.lower()
        text = text.replace(',', ' ')
        text = text.replace('.', ' ')
        text = text.replace('#', '')
        if not self._accents:
            text = self.__strip_accents(text, 'utf-8')

        utext = unicode(text, 'utf8')
        words = self._tokenizer.tokenize(utext)  
        return words

    def _filter_words(self, in_words):
        words = list(in_words)

        for stop in self._stop_words:
            words = filter(lambda a: a != stop, words)
        
        words = filter(lambda a: len(a) >= self._min_length, words)
        words = filter(lambda a: not a.startswith(u'http'), words)
        words = filter(lambda a: not '/' in a, words)
        return words

    def __not_combining(self, char):
        return unicodedata.category(char) != 'Mn'
    
    def __strip_accents(self, text, encoding):
        if isinstance(text, str):
            text = unicode(text, encoding)
        unicode_text= unicodedata.normalize('NFD', text)
        return filter(self.__not_combining, unicode_text).encode(encoding)


QUERY = ' OR '.join(map(lambda x: "("+x+")", phrases)) + ' +exclude:retweets'

corpus = Corpus(cz_stop, min_length=3)

for page in range(1, NUM_PAGES+1):
    base_url = 'http://search.twitter.com/search.json?q=%s&rpp=%s&page=%s&lang=pl' \
         % (urllib2.quote(QUERY), RESULTS_PER_PAGE, page)
    results_json = simplejson.loads(scraperwiki.scrape(base_url))
    for result in results_json['results']:
        corpus.add_document(result['text'])


#scraperwiki.sqlite.execute("drop table most_common")
scraperwiki.sqlite.execute("create table if not exists most_common (tstam timestamp, word varchar, count int)")

most_common = corpus.get_counts().most_common(10)

for word, count in most_common:
    scraperwiki.sqlite.execute("insert into most_common values (DATETIME('now'),?, ?)", (word, count))

scraperwiki.sqlite.commit()   
