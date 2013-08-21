import scraperwiki
import lxml.html 
import json
import re

print "getlinks"
#scraperwiki.sqlite.execute("drop table pages")

urlbase="https://pluragraph.de/categories/kultur/page/"
page=1

while page<1000:
    print page
    html = scraperwiki.scrape(urlbase+str(page))
    if not html: break
    
    root = lxml.html.fromstring(html) 
    rows=root.cssselect("table.organisation_listing tr")
    rows.pop(0)
    if len(rows)==0: break

    for tr in rows:
        link = tr.cssselect("td.details a")
        data = {'page':page,'name':link[0].text_content().encode('iso-8859-1'),'detaillink':link[0].get("href")}
        #print data
        scraperwiki.sqlite.save(unique_keys=['name'], data=data,table_name="pages")

    page+=1


print "get profiles"
#scraperwiki.sqlite.execute("drop table profiles")
urlbase="https://pluragraph.de"
page=0
while page<1000:
    print page

    orgas=scraperwiki.sqlite.execute("select * from pages limit 50 offset "+str(page*50))
    if len(orgas['data'])==0: break
    
    for org in orgas['data']:
        html = scraperwiki.scrape(urlbase+org[1])
        if not html: break

        root = lxml.html.fromstring(html)
        profiles=root.cssselect("table.profiles_listing tr td.name a.facebook")
        if len(profiles) > 0:            
            profurl=profiles[0].get("href")
            profmain=1 if profiles[0].getparent().text_content().find('(Hauptprofil)')>-1 else 0
            profcount=len(profiles)
            
            profall=[]
            for prof in profiles:                
                s_profurl=prof.get("href")
                s_main=1 if prof.getparent().text_content().find('(Hauptprofil)')>-1 else 0
                profall.append({'url':s_profurl,'main':s_main})
                if s_main==1:
                    profurl=s_profurl
                    profmain=s_main
            
            data = {'name':org[2],'detaillink':org[1],'facebook':profurl,'facebookmain':profmain,'facebookcount':profcount,'facebookall':json.dumps(profall)}    
            scraperwiki.sqlite.save(unique_keys=['detaillink'], data=data,table_name="profiles")
        else:
            data = {'name':org[2],'detaillink':org[1],'facebookcount':0}    
            scraperwiki.sqlite.save(unique_keys=['detaillink'], data=data,table_name="profiles")

    page+=1





