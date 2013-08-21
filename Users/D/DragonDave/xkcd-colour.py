import scraperwiki

# Blank Python
lc=scraperwiki.swimport('lazycache')

url='http://xkcd.com/color/rgb.txt'
text=lc.lazycache(url)
data=[]
for row in text.split('\n')[:-1]:
    z=row.split('\t')
    data.append({'name':z[0],'colour':z[1]})
scraperwiki.sqlite.save(data=data,unique_keys=[],table_name='colour')
