import scraperwiki

scraperwiki.sqlite.execute('drop table if exists ttt')

html = scraperwiki.scrape("http://www.thatvideosite.com/")

pos1=0
pos2=0
data=[]
while pos1>-1:
    pos1=html.find('src="http://media.thatvideosite.com/core/', pos2 + 1)
    pos2=html.find('/', pos1 + 42)
    if pos1==-1:
        break
    id = html[pos1+41:pos2]
    pos1=html.find('style="font-size: 1.4em;">', pos2 + 1)
    pos2=html.find('</a>', pos1 + 26)
    if pos1==-1:
        break
    title = html[pos1+26:pos2]
    
    data.append( {
        'title' : title.replace(',', '&COMMA;'),
        'id' : 'http://www.thatvideosite.com/core/' + id + '/video.flv'
    } )



scraperwiki.sqlite.save(unique_keys=['id'], data=data)