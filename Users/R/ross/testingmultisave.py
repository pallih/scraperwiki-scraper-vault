import scraperwiki

# Blank Python

buff = []
for x in range(100000):
    d = dict(id=1,val=x,val1=x, val2=x, val3=x)
    buff.append(d)
    if len(buff) % 500 == 0:
        scraperwiki.sqlite.save( ['id'], buff )
        buff = []
