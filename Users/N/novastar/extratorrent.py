import scraperwiki
import lxml.html

#START


tcount = 1

html = scraperwiki.scrape('http://extratorrent.com/torrent_trackers/2911043/Sushi+Girl+2012+720p+WEB-DL+DD5+1+H+264-BS.html')
root = lxml.html.fromstring(html)



tleech= root.cssselect('H2 span.leech')[1].text_content()
tseed= root.cssselect('H2 span.seed')[1].text_content()
    
torrent  = {
    'seed' : tseed,
    'leech' : tleech,
    'id' : '1'
}
print scraperwiki.sqlite.save(unique_keys=['id'], data=torrent)

#break

print tcount 
#break
    
    
