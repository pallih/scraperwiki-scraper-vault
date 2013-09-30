import scraperwiki

# Blank Python

def makedata():
    testdata=[['bob',21,22],
            ['jeff',9,99],
            ['chris',12,-1],
            ['dom',1001,3030]]

    data = [dict(zip(['name','w1','w2'], x)) for x in testdata]

    scraperwiki.sqlite.save(data=data, unique_keys=[])

print scraperwiki.sqlite.select ('* from swdata order by w1')import scraperwiki

# Blank Python

def makedata():
    testdata=[['bob',21,22],
            ['jeff',9,99],
            ['chris',12,-1],
            ['dom',1001,3030]]

    data = [dict(zip(['name','w1','w2'], x)) for x in testdata]

    scraperwiki.sqlite.save(data=data, unique_keys=[])

print scraperwiki.sqlite.select ('* from swdata order by w1')