# Blank Python
sourcescraper = 'finance_twitter'

import scraperwiki, string, re     

# Grab yoself some data
scraperwiki.sqlite.attach("finance_twitter")
data = scraperwiki.sqlite.select(           
    '''text from swdata'''
)

# remove non alpha numeric
pattern = re.compile('[\W]', re.U)


# make a long old list
longlistoftext = []

for item in data:
    itemtext = item['text']
    #itemtext = pattern.sub('', itemtext)
    
    words = itemtext.split(' ')
    for word in words:
        word = pattern.sub('', word)
        if len(word) > 0:
            longlistoftext.append(word)

longlistoftext.sort()

for text in longlistoftext:
    print text+'<br />'
# Blank Python
sourcescraper = 'finance_twitter'

import scraperwiki, string, re     

# Grab yoself some data
scraperwiki.sqlite.attach("finance_twitter")
data = scraperwiki.sqlite.select(           
    '''text from swdata'''
)

# remove non alpha numeric
pattern = re.compile('[\W]', re.U)


# make a long old list
longlistoftext = []

for item in data:
    itemtext = item['text']
    #itemtext = pattern.sub('', itemtext)
    
    words = itemtext.split(' ')
    for word in words:
        word = pattern.sub('', word)
        if len(word) > 0:
            longlistoftext.append(word)

longlistoftext.sort()

for text in longlistoftext:
    print text+'<br />'
