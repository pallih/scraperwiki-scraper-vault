"""Natural Language Toolkit is installed on ScraperWiki: http://www.nltk.org/
Please try it out and do something excellent with it.
"""

# Work through the book given here:  http://nltk.googlecode.com/svn/trunk/doc/book/ch05.html

import nltk

# there are some big books (maybe load only the one you want)
if False:
    import nltk.book
    print help(nltk.book)
    print nltk.book.texts()
    print nltk.book.sents()
    print nltk.book.text6.collocations(num=20, window_size=2)

    #nltk.book.text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])
#nltk.stem.porter.demo()
#nltk.stem.lancaster.demo()

# corpus stuff 
text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
print text
print text.similar('woman')


# some grammar parsing
if False:
    sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
    groucho_grammar = nltk.parse_cfg("""
     S -> NP VP
     PP -> P NP
     NP -> Det N | Det N PP | 'I'
     VP -> V NP | VP PP
     Det -> 'an' | 'my'
     N -> 'elephant' | 'pajamas'
     V -> 'shot'
     P -> 'in'
    """)
    
    parser = nltk.ChartParser(groucho_grammar)
    trees = parser.nbest_parse(sent)
    for tree in trees:
        print str(tree)+"    ."*8

"""Natural Language Toolkit is installed on ScraperWiki: http://www.nltk.org/
Please try it out and do something excellent with it.
"""

# Work through the book given here:  http://nltk.googlecode.com/svn/trunk/doc/book/ch05.html

import nltk

# there are some big books (maybe load only the one you want)
if False:
    import nltk.book
    print help(nltk.book)
    print nltk.book.texts()
    print nltk.book.sents()
    print nltk.book.text6.collocations(num=20, window_size=2)

    #nltk.book.text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])
#nltk.stem.porter.demo()
#nltk.stem.lancaster.demo()

# corpus stuff 
text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
print text
print text.similar('woman')


# some grammar parsing
if False:
    sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
    groucho_grammar = nltk.parse_cfg("""
     S -> NP VP
     PP -> P NP
     NP -> Det N | Det N PP | 'I'
     VP -> V NP | VP PP
     Det -> 'an' | 'my'
     N -> 'elephant' | 'pajamas'
     V -> 'shot'
     P -> 'in'
    """)
    
    parser = nltk.ChartParser(groucho_grammar)
    trees = parser.nbest_parse(sent)
    for tree in trees:
        print str(tree)+"    ."*8

"""Natural Language Toolkit is installed on ScraperWiki: http://www.nltk.org/
Please try it out and do something excellent with it.
"""

# Work through the book given here:  http://nltk.googlecode.com/svn/trunk/doc/book/ch05.html

import nltk

# there are some big books (maybe load only the one you want)
if False:
    import nltk.book
    print help(nltk.book)
    print nltk.book.texts()
    print nltk.book.sents()
    print nltk.book.text6.collocations(num=20, window_size=2)

    #nltk.book.text4.dispersion_plot(["citizens", "democracy", "freedom", "duties", "America"])
#nltk.stem.porter.demo()
#nltk.stem.lancaster.demo()

# corpus stuff 
text = nltk.Text(word.lower() for word in nltk.corpus.brown.words())
print text
print text.similar('woman')


# some grammar parsing
if False:
    sent = ['I', 'shot', 'an', 'elephant', 'in', 'my', 'pajamas']
    groucho_grammar = nltk.parse_cfg("""
     S -> NP VP
     PP -> P NP
     NP -> Det N | Det N PP | 'I'
     VP -> V NP | VP PP
     Det -> 'an' | 'my'
     N -> 'elephant' | 'pajamas'
     V -> 'shot'
     P -> 'in'
    """)
    
    parser = nltk.ChartParser(groucho_grammar)
    trees = parser.nbest_parse(sent)
    for tree in trees:
        print str(tree)+"    ."*8

