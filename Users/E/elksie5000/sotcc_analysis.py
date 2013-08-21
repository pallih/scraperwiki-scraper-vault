import scraperwiki
import pandas as pd
import nltk
from nltk.metrics import BigramAssocMeasures
from nltk.metrics import TrigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.collocations import TrigramCollocationFinder


scraperwiki.sqlite.attach("sotcc_processed_quotes")
quotes_data =  scraperwiki.sqlite.select("* from sotcc_processed_quotes.swdata")
scraperwiki.sqlite.attach("sotcc_cabinet")
cabinet_data =  scraperwiki.sqlite.select("Councillor from sotcc_cabinet.swdata")

df = pd.DataFrame(quotes_data)



for coun in cabinet_data:
    row = {}
    comb_quote =""
    raw_quote = ""
    for quote in quotes_data:
        row['councillor'] = coun['Councillor']
        if quote['subject'] == coun['Councillor']:
            comb_quote += " "+quote['quote_clean'].lower()
            raw_quote += " "+quote['quote_clean']

    
    
    words = []
    
    
    #break into sentences
    sentences = nltk.tokenize.sent_tokenize(raw_quote)
    

    #now break sentences into tokens
    tokens = [nltk.word_tokenize(s) for s in sentences]
    
    
    #A bit of POS tagging
    pos_tagged_tokens = [nltk.pos_tag(t) for t in tokens]

    #Chunk extraction time
    ne_chunks = nltk.batch_ne_chunk(pos_tagged_tokens)

    # Flatten the list since we're not using sentence structure
    # and sentences are guaranteed to be separated by a special
    # POS tuple such as ('.', '.')
    pos_tagged_tokens = [token for sent in pos_tagged_tokens for token in sent]
    print type(pos_tagged_tokens)
    pos_tagged_tokens
   
    
    
    words = [w.lower() for sentence in sentences for w in nltk.word_tokenize(sentence)]
    
    #Basic lexical diversity measures
    length_words = len(words)
    print length_words
    unique_words = len(set(words))

    #Entity extraction
    
    #Code from Mining data from the social web: https://github.com/ptwobrussell/Mining-the-Social-Web/blob/master/python_code/blogs_and_nlp__extract_entities.py
    post = {}
    all_entity_chunks = []
    previous_pos = None
    current_entity_chunk = []
    print pos_tagged_tokens
    for (token, pos) in pos_tagged_tokens:

        if pos == previous_pos and pos.startswith('NN'):
            current_entity_chunk.append(token)
        elif pos.startswith('NN'):
            if current_entity_chunk != []:

                # Note that current_entity_chunk could be a duplicate when appended,
                # so frequency analysis again becomes a consideration

                all_entity_chunks.append((' '.join(current_entity_chunk), pos))
            current_entity_chunk = [token]

        previous_pos = pos

    # Store the chunks as an index for the document
    # and account for frequency while we're at it...

    post['entities'] = {}
    for c in all_entity_chunks:
        post['entities'][c] = post['entities'].get(c, 0) + 1

    # For example, we could display just the title-cased entities

    
    proper_nouns = []
    for (entity, pos) in post['entities']:
        if entity.istitle():
            print '\t%s (%s)' % (entity, post['entities'][(entity, pos)])
            continue
    
    lexical_diversity = 1.0*unique_words/length_words
    row['length_words'] = length_words
    row['unique_words'] = unique_words
    row['lexical_diversity'] = lexical_diversity
    row['words_bulk'] = raw_quote
    
    freq_dist = nltk.FreqDist(words)
    print freq_dist.keys()[:50] #top 50 most frequent tokens
    print freq_dist.keys()[-50:] #top 50 least frequent tokens       
    print "facilitate count:"
    print freq_dist['facilitate']

    #Hapaxes
    num_hapaxes = len(freq_dist.hapaxes())
    print "Hapaxes: "+ str(num_hapaxes)
   
    #Let's look for bigrams    
    bcf = BigramCollocationFinder.from_words(words)
    row['bcf'] = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 10)
    #...And trigrams
    tcf = TrigramCollocationFinder.from_words(words)
    row['tcf'] = tcf.nbest(TrigramAssocMeasures.likelihood_ratio, 10)

    #now let's remove the stopwords and remove punctuation
    from nltk.corpus import stopwords
    stopset = set(stopwords.words('english'))
    filter_stops = lambda w: len(w) <3 or w in stopset
    bcf.apply_word_filter(filter_stops)
    row['filtered_bcf'] = bcf.nbest(BigramAssocMeasures.likelihood_ratio, 10)
    
    


    scraperwiki.sqlite.save(unique_keys=['councillor'], data=row)
    


