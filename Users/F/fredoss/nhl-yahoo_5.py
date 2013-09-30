import scraperwiki
import requests
import lxml.html
import re

def duckint(i):
    try:
        return int(i)
    except ValueError:
        return i

# Blank Python
lookup = ['NAME','TEAM','GP','G','A','PTS']
num =    [0,1,2,4,6,8]

lstring = ', '.join(lookup)

scraperwiki.sqlite.execute('create table if not exists STATS13 (%s)'%lstring)

url='http://sports.yahoo.com/nhl/stats/byposition?pos=C,RW,LW,D,G'
html=requests.get(url).content
root=lxml.html.fromstring(html)

rows=root.xpath('//table[@class="yspcontent"]//tr[@class="ysprow1" or @class="ysprow2"]')
builder=[]
for row in rows:
    data={}
    cells=[cell.text_content().strip() for cell in row.xpath('td[@class="yspscores"]')]
    for i,n in enumerate(num):
        data[lookup[i]]=duckint(cells[n])
    data['PTS']=duckint(row.xpath('descendant-or-self::span[@class="yspscores"]')[0].text_content().strip())
    builder.append(data)
    
scraperwiki.sqlite.save(table_name='STATS13', data=builder, unique_keys=['NAME'])
import scraperwiki
import requests
import lxml.html
import re

def duckint(i):
    try:
        return int(i)
    except ValueError:
        return i

# Blank Python
lookup = ['NAME','TEAM','GP','G','A','PTS']
num =    [0,1,2,4,6,8]

lstring = ', '.join(lookup)

scraperwiki.sqlite.execute('create table if not exists STATS13 (%s)'%lstring)

url='http://sports.yahoo.com/nhl/stats/byposition?pos=C,RW,LW,D,G'
html=requests.get(url).content
root=lxml.html.fromstring(html)

rows=root.xpath('//table[@class="yspcontent"]//tr[@class="ysprow1" or @class="ysprow2"]')
builder=[]
for row in rows:
    data={}
    cells=[cell.text_content().strip() for cell in row.xpath('td[@class="yspscores"]')]
    for i,n in enumerate(num):
        data[lookup[i]]=duckint(cells[n])
    data['PTS']=duckint(row.xpath('descendant-or-self::span[@class="yspscores"]')[0].text_content().strip())
    builder.append(data)
    
scraperwiki.sqlite.save(table_name='STATS13', data=builder, unique_keys=['NAME'])
