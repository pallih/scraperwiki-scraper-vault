import scraperwiki

# Blank Python
lis = []
for i in range(0,10):
    scraperwiki.sqlite.save(unique_keys=['country'], data=i) 

