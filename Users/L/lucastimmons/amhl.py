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
lookup = ['No.','Pos','Player','Team','GP','G','A','PTS','GWG','GTG','PPG','SHG','ENG','PIM']
num =    [0,1,2,3,4,5,6,7,8,9,10,11,12,13]

lstring = ', '.join(lookup)

scraperwiki.sqlite.execute('create table if not exists stats (%s)'%lstring)
url='http://amhl.ab.ca/leaderboard_skater.php?season_id=1'
html=requests.get(url).content
root=lxml.html.fromstring(html)

rows=root.xpath('//tr[@class="altrow" or @class="normrow"]')
builder=[]
for row in rows:
    data={}
    cells=[cell.text_content().strip() for cell in row.xpath('td[@class=""]')]
    for i,n in enumerate(num):
        data[lookup[i]]=duckint(cells[n])
    builder.append(data)
    
scraperwiki.sqlite.save(table_name='stats', data=builder, unique_keys=['No.'])