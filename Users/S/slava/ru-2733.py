import scraperwiki
import lxml.html
import re
import demjson

# Blank Python

#Enter a wrong link, and you'll get all office links. Like they couldn't post that in first place >:(
offices_links="""/offices/office/155/
/offices/office/4245/
/offices/office/6/
/offices/office/168/
/offices/office/165/
/offices/office/153/
/offices/office/442/
/offices/office/181/
/offices/office/9/
/offices/office/440/
/offices/office/443/
/offices/office/167/
/offices/office/160/
/offices/office/8/
/offices/office/163/
/offices/office/1425/
/offices/office/1841/
/offices/office/154/
/offices/office/166/
/offices/office/145/
/offices/office/183/
/offices/office/162/
/offices/office/1162/
/offices/office/158/
/offices/office/10/
/offices/office/441/
/offices/office/156/
/offices/office/186/
/offices/office/169/
/offices/office/189/
/offices/office/159/
/offices/office/2534/
/offices/office/152/
/offices/office/164/
/offices/office/187/
/offices/office/184/
/offices/office/179/
/offices/office/444/
/offices/office/2188/
/offices/office/157/
/offices/office/185/
/offices/office/1745/
/offices/office/180/
/offices/office/161/
/offices/office/188/
/offices/office/182/
/offices/office/146/
/offices/office/190/"""

scraperwiki.sqlite.execute('delete from branches')
i=1
for office in offices_links.split("\n"):
    data={'id':i,'lat':'','lon':''}
    office=office.strip()
    html=scraperwiki.scrape("http://www.pskb.com"+office)
    html=html.decode('windows-1251')
    root=lxml.html.document_fromstring(html)
    content=root.xpath("//div[@class='alpha grid_12 content']")
    print content[0].text_content()
    
    data['branch_name']=content[0].xpath('h1')[0].text_content()
    data['branch_address']=content[0].xpath("div[@class='office-detail']/h2[1]")[0].text_content()
    ll=re.findall(r'startPoint = new\sYMaps\.GeoPoint\(([\d\.]+?),([\d\.]+?)\)',html,re.I|re.U)

    if ll!=[] and len(ll[0])==2:
        data['lat']=ll[0][1]
        data['lon']=ll[0][0]

    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="branches")
    i+=1

    
    


    

import scraperwiki
import lxml.html
import re
import demjson

# Blank Python

#Enter a wrong link, and you'll get all office links. Like they couldn't post that in first place >:(
offices_links="""/offices/office/155/
/offices/office/4245/
/offices/office/6/
/offices/office/168/
/offices/office/165/
/offices/office/153/
/offices/office/442/
/offices/office/181/
/offices/office/9/
/offices/office/440/
/offices/office/443/
/offices/office/167/
/offices/office/160/
/offices/office/8/
/offices/office/163/
/offices/office/1425/
/offices/office/1841/
/offices/office/154/
/offices/office/166/
/offices/office/145/
/offices/office/183/
/offices/office/162/
/offices/office/1162/
/offices/office/158/
/offices/office/10/
/offices/office/441/
/offices/office/156/
/offices/office/186/
/offices/office/169/
/offices/office/189/
/offices/office/159/
/offices/office/2534/
/offices/office/152/
/offices/office/164/
/offices/office/187/
/offices/office/184/
/offices/office/179/
/offices/office/444/
/offices/office/2188/
/offices/office/157/
/offices/office/185/
/offices/office/1745/
/offices/office/180/
/offices/office/161/
/offices/office/188/
/offices/office/182/
/offices/office/146/
/offices/office/190/"""

scraperwiki.sqlite.execute('delete from branches')
i=1
for office in offices_links.split("\n"):
    data={'id':i,'lat':'','lon':''}
    office=office.strip()
    html=scraperwiki.scrape("http://www.pskb.com"+office)
    html=html.decode('windows-1251')
    root=lxml.html.document_fromstring(html)
    content=root.xpath("//div[@class='alpha grid_12 content']")
    print content[0].text_content()
    
    data['branch_name']=content[0].xpath('h1')[0].text_content()
    data['branch_address']=content[0].xpath("div[@class='office-detail']/h2[1]")[0].text_content()
    ll=re.findall(r'startPoint = new\sYMaps\.GeoPoint\(([\d\.]+?),([\d\.]+?)\)',html,re.I|re.U)

    if ll!=[] and len(ll[0])==2:
        data['lat']=ll[0][1]
        data['lon']=ll[0][0]

    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="branches")
    i+=1

    
    


    

