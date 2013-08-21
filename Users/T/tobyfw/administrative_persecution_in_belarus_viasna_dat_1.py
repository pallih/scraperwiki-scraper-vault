import lxml.html          
import scraperwiki 
import dateutil.parser 
import re
import sys

entryRe = '<p align="center">(.+?)<br>(.+?)<br>(.+?)</p>'
# addressRe = '([0-9]+?)[, ]*(.+?),(.+?),(.+?)'

# download one page 
def get_page(area, url):
    html = scraperwiki.scrape(url) 
    root = lxml.html.fromstring(html)

    td = root.cssselect("td.news_text")[0]  

    for p in td.cssselect("p"):       
        entry = lxml.html.tostring(p, encoding=unicode)
        els = re.findall(entryRe, entry)

        if len(els) == 1 and len(els[0]) == 3:
            courtHtml = lxml.html.fromstring(els[0][0])
            addressHtml = lxml.html.fromstring(els[0][1])
            telephoneHtml = lxml.html.fromstring(els[0][2])
            data = {
                'Court' : courtHtml.text_content(),
                'Address' : addressHtml.text_content(),
                'Telephone' : telephoneHtml.text_content(),
                'District' : area
            }
            scraperwiki.sqlite.save(unique_keys=['Court'], data=data)
        else:
            print "Not parsed: " + entry

get_page( "Город минск", "http://www.minjust.by/ru/info/minsk/new_url_576144963" ) 
get_page( "Брестская область", "http://www.minjust.by/ru/info/brest_obl/new_url_645081743" ) 
get_page( "Витебская область", "http://www.minjust.by/ru/info/vitebsk_obl/sudy" ) 
get_page( "Гомельская область", "http://www.minjust.by/ru/info/gomel_obl/sudy" ) 
get_page( "Гродненская область", "http://www.minjust.by/ru/info/grodno_obl/sudy" ) 
get_page( "Минская область", "http://www.minjust.by/ru/info/minsk_obl/sudy" ) 
get_page( "Могилевская область", "http://www.minjust.by/ru/info/mogilev_obl/sudy" )



