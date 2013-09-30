import scraperwiki
import re
# Blank Python

#http://www.itb.ru/branches_and_offices/affiliates/

#html=scraperwiki.scrape("https://dl.dropbox.com/u/14865435/2733-data.txt")
html=scraperwiki.scrape("http://www.itb.ru/branches_and_offices/affiliates/")
html=html.decode('windows-1251')
points=re.findall(r'(?:\n|\r)[^/]*?placemark(\d{3}).*?=.*?new YMaps\.Placemark\(new YMaps\.GeoPoint\(([\d\.]+?),([\d\.]+?)\)', html, re.I|re.U)
texts=re.findall(r"(?:\n|\r)[^/]*?textition(\d{3}).*?=.*?'(.*?)';", html, re.I|re.U)
names=re.findall(r"(?:\n|\r)[^/]*?placemark(\d{3})\.name.*?=.*?'(.*?)';", html, re.I|re.U)
descriptions=re.findall(r"(?:\n|\r)[^/]*?placemark(\d{3})\.description.*?=.*?(?:'|"")(.*?)(?:'|"");", html, re.I|re.U)

print texts

print len(points), len(texts), len(names), len(descriptions)
for e in range(0,len(points)+1):
    scraperwiki.sqlite.save(unique_keys=['point_id'], 
        data={'point_id': points[e][0], 
            'lat':points[e][1], 
            'lon':points[e][2], 
            'text_id':texts[e][0],
            'text':texts[e][1],
            'name_id': names[e][0],
            'name': names[e][1],
            'description_id': descriptions[e][0],
            'description': descriptions[e][1]}, table_name='by_map')import scraperwiki
import re
# Blank Python

#http://www.itb.ru/branches_and_offices/affiliates/

#html=scraperwiki.scrape("https://dl.dropbox.com/u/14865435/2733-data.txt")
html=scraperwiki.scrape("http://www.itb.ru/branches_and_offices/affiliates/")
html=html.decode('windows-1251')
points=re.findall(r'(?:\n|\r)[^/]*?placemark(\d{3}).*?=.*?new YMaps\.Placemark\(new YMaps\.GeoPoint\(([\d\.]+?),([\d\.]+?)\)', html, re.I|re.U)
texts=re.findall(r"(?:\n|\r)[^/]*?textition(\d{3}).*?=.*?'(.*?)';", html, re.I|re.U)
names=re.findall(r"(?:\n|\r)[^/]*?placemark(\d{3})\.name.*?=.*?'(.*?)';", html, re.I|re.U)
descriptions=re.findall(r"(?:\n|\r)[^/]*?placemark(\d{3})\.description.*?=.*?(?:'|"")(.*?)(?:'|"");", html, re.I|re.U)

print texts

print len(points), len(texts), len(names), len(descriptions)
for e in range(0,len(points)+1):
    scraperwiki.sqlite.save(unique_keys=['point_id'], 
        data={'point_id': points[e][0], 
            'lat':points[e][1], 
            'lon':points[e][2], 
            'text_id':texts[e][0],
            'text':texts[e][1],
            'name_id': names[e][0],
            'name': names[e][1],
            'description_id': descriptions[e][0],
            'description': descriptions[e][1]}, table_name='by_map')