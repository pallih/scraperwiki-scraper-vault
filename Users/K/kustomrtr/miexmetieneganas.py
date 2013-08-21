import scraperwiki  
import lxml.html
import re
        
html = scraperwiki.scrape("http://www.youtube.com/user/MiExmeTieneganas/videos")
root = lxml.html.fromstring(html)

for el in root.cssselect("h3.yt-c3-grid-item-title a"):
    titulo_raw = re.sub('(?i)Mi Ex Me Tiene Ganas', '', el.text)
    titulo_final = re.sub('(?i)\s-\s', '', titulo_raw)
    url = "http://linkyoutube.com" + el.attrib['href']
    #print titulo_final, url

    if titulo_final.find("tulo") > 0:
        data = {
            'title' : titulo_final,
            'url' : url
               }
        scraperwiki.sqlite.save(unique_keys=['url'], data=data)


#if el.attrib['href'].find("imgur") > 0:
