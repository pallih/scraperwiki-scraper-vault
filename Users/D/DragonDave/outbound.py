import scraperwiki

# Blank Python

h=scraperwiki.scrape('http://176.58.117.72:7822/outbound.txt')
items=h.strip().split('\n')

data=[{'outbound':x} for x in items]
scraperwiki.sqlite.save(table_name='outbound', data=data, unique_keys=['outbound'])

###############################

"""
import csv, os
d={}
for i in os.listdir('Code-Point Open/Data'):
    fn='Code-Point Open/Data/'+i
    fh=open(fn)
    data=fh.read().split('\n')
    for i in data:
        out=i.partition(',')[0].replace('"','')[:4].strip()
        d[out]=True
print '\n'.join(sorted(d))
"""
import scraperwiki

# Blank Python

h=scraperwiki.scrape('http://176.58.117.72:7822/outbound.txt')
items=h.strip().split('\n')

data=[{'outbound':x} for x in items]
scraperwiki.sqlite.save(table_name='outbound', data=data, unique_keys=['outbound'])

###############################

"""
import csv, os
d={}
for i in os.listdir('Code-Point Open/Data'):
    fn='Code-Point Open/Data/'+i
    fh=open(fn)
    data=fh.read().split('\n')
    for i in data:
        out=i.partition(',')[0].replace('"','')[:4].strip()
        d[out]=True
print '\n'.join(sorted(d))
"""
