import scraperwiki
import nltk
from nltk import pos_tag, word_tokenize
from nltk.collocations import *
from nltk.corpus import *
import re

def nltk_nouns(val):
    val = re.sub('[\[\]\|\!\$\%\&\(\)\-\_\=\+\\\/]+', ' ', val)
    tokens = nltk.word_tokenize(val)
    tagged = nltk.pos_tag(tokens)
    nouns = []
    for tag in tagged:
        item, typ = tag
        if typ == 'NNP' or typ == 'NN':
            nouns.append(item)
    #logging.info('nouns: ' + repr(nouns))
    return ' '.join(nouns)

#Venezia
scraperwiki.sqlite.attach("comunevenezia_determinazioni2012", "src")           
#print scraperwiki.sqlite.table_info("src.swdata")
venItems = scraperwiki.sqlite.select("* from src.swdata where anno = 2012")


bigram_measures = nltk.collocations.BigramAssocMeasures()

# change this to read in your data
finder = BigramCollocationFinder.from_words(nltk.corpus.genesis.words('english-web.txt'))

# only bigrams that appear 3+ times
finder.apply_freq_filter(3) 

# return the 5 n-grams with the highest PMI
print(finder.nbest(bigram_measures.pmi, 50)  )

testo = ''

for delibera in venItems: 
    #print delibera

    # change this to read in your data
    #print(word_tokenize(delibera['descrizione']))
    
    testo = testo + nltk_nouns(delibera['descrizione'])
    
    #print(word_tokenize()

    # return the 5 n-grams with the highest PMI
    #print( finder.nbest(bigram_measures.pmi, 5) )

    data = {
           'codiceIstat' : 27042,
           'comune' : 'Venezia',
           'num' : delibera['num'],
           'codice' : delibera['codice'],
            'categoria': "",
           'importo' : delibera['importo'] ,
           'anno' : delibera['anno'],
           'descrizione' : delibera['descrizione'],
           'DataSalvataggio' : delibera['DataSalvataggio'],
           'DataUltimoUpdate' : delibera['DataUltimoUpdate'],
           'url' : delibera['url']
    }
    #print data
    
    #scraperwiki.sqlite.save(unique_keys=['codice'], data=data)

fd = nltk.FreqDist()
for word in nltk.word_tokenize(testo):
     fd.inc(word)

print(fd)

#finder = BigramCollocationFinder.from_words(word_tokenize(testo))

#finder.apply_freq_filter(3) 

#print(testo)

# return the 5 n-grams with the highest PMI
#print( finder.nbest(bigram_measures.pmi, 50) )

#finder = BigramCollocationFinder.from_words( word_tokenize(

#finder.apply_freq_filter(3) 
    
# return the 5 n-grams with the highest PMI
#print( finder.nbest(bigram_measures.pmi, 15))
         

