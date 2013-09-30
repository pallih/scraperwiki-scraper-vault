# Blank Python

import nltk.corpus, nltk.tag, itertools 

brown_review_sents = nltk.corpus.brown.tagged_sents(categories=['reviews']) 
#brown_lore_sents = nltk.corpus.brown.tagged_sents(categories=['lore']) 
#brown_romance_sents = nltk.corpus.brown.tagged_sents(categories=['romance'])   
#brown_train = list(itertools.chain(brown_review_sents[:1000], brown_lore_sents[:1000], brown_romance_sents[:1000])) 
#brown_test = list(itertools.chain(brown_review_sents[1000:2000], brown_lore_sents[1000:2000], brown_romance_sents[1000:2000]))   
#conll_sents = nltk.corpus.conll2000.tagged_sents() 
##conll_train = list(conll_sents[:4000]) 
#conll_test = list(conll_sents[4000:8000])   
##treebank_sents = nltk.corpus.treebank.tagged_sents() 
#treebank_train = list(treebank_sents[:1500]) 
#treebank_test = list(treebank_sents[1500:3000]) 

def backoff_tagger(tagged_sents, tagger_classes, backoff=None):
    if not backoff:         
        backoff = tagger_classes[0](tagged_sents)         
        del tagger_classes[0]       
    for cls in tagger_classes:         
        tagger = cls(tagged_sents, backoff=backoff)         
        backoff = tagger      
    return backoff 

ubt_tagger = backoff_tagger(brown_review_sents, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger]) 
#utb_tagger = backoff_tagger(brown_review_sents, [nltk.tag.UnigramTagger, nltk.tag.TrigramTagger, nltk.tag.BigramTagger]) 
#but_tagger = backoff_tagger(brown_review_sents, [nltk.tag.BigramTagger, nltk.tag.UnigramTagger, nltk.tag.TrigramTagger]) 
#btu_tagger = backoff_tagger(brown_review_sents, [nltk.tag.BigramTagger, nltk.tag.TrigramTagger, nltk.tag.UnigramTagger]) 
#tub_tagger = backoff_tagger(brown_review_sents, [nltk.tag.TrigramTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger]) 
#tbu_tagger = backoff_tagger(brown_review_sents, [nltk.tag.TrigramTagger, nltk.tag.BigramTagger, nltk.tag.UnigramTagger]) 

print(ubt_tagger)


# Blank Python

import nltk.corpus, nltk.tag, itertools 

brown_review_sents = nltk.corpus.brown.tagged_sents(categories=['reviews']) 
#brown_lore_sents = nltk.corpus.brown.tagged_sents(categories=['lore']) 
#brown_romance_sents = nltk.corpus.brown.tagged_sents(categories=['romance'])   
#brown_train = list(itertools.chain(brown_review_sents[:1000], brown_lore_sents[:1000], brown_romance_sents[:1000])) 
#brown_test = list(itertools.chain(brown_review_sents[1000:2000], brown_lore_sents[1000:2000], brown_romance_sents[1000:2000]))   
#conll_sents = nltk.corpus.conll2000.tagged_sents() 
##conll_train = list(conll_sents[:4000]) 
#conll_test = list(conll_sents[4000:8000])   
##treebank_sents = nltk.corpus.treebank.tagged_sents() 
#treebank_train = list(treebank_sents[:1500]) 
#treebank_test = list(treebank_sents[1500:3000]) 

def backoff_tagger(tagged_sents, tagger_classes, backoff=None):
    if not backoff:         
        backoff = tagger_classes[0](tagged_sents)         
        del tagger_classes[0]       
    for cls in tagger_classes:         
        tagger = cls(tagged_sents, backoff=backoff)         
        backoff = tagger      
    return backoff 

ubt_tagger = backoff_tagger(brown_review_sents, [nltk.tag.UnigramTagger, nltk.tag.BigramTagger, nltk.tag.TrigramTagger]) 
#utb_tagger = backoff_tagger(brown_review_sents, [nltk.tag.UnigramTagger, nltk.tag.TrigramTagger, nltk.tag.BigramTagger]) 
#but_tagger = backoff_tagger(brown_review_sents, [nltk.tag.BigramTagger, nltk.tag.UnigramTagger, nltk.tag.TrigramTagger]) 
#btu_tagger = backoff_tagger(brown_review_sents, [nltk.tag.BigramTagger, nltk.tag.TrigramTagger, nltk.tag.UnigramTagger]) 
#tub_tagger = backoff_tagger(brown_review_sents, [nltk.tag.TrigramTagger, nltk.tag.UnigramTagger, nltk.tag.BigramTagger]) 
#tbu_tagger = backoff_tagger(brown_review_sents, [nltk.tag.TrigramTagger, nltk.tag.BigramTagger, nltk.tag.UnigramTagger]) 

print(ubt_tagger)


