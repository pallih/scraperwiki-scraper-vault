import scraperwiki
import lxml.html
import demjson


html=scraperwiki.scrape("http://www.atu.de/pages/shop/ekat/ekat.html")
root=lxml.html.document_fromstring(html)
scraperwiki.sqlite.execute("delete from data")
id=1
for el in root.xpath("//select[@name='selHersteller']/option"):
    #print el.attrib['value'] + ", " + el.text_content();
    if el.attrib['value'] =="" : continue
    data=[{'id':id, 'title': el.text_content(), 'parent_id':'', 'site_id':el.attrib['value'] }]
    parent_id=id
    id+=1
    html=scraperwiki.scrape("http://www.atu.de/de/content/shop/ekat/getkfzmodelle.jsp?selHersteller="+el.attrib['value']+"&rnd=63763")
    json=demjson.decode(html)
    #print json
    for model in json['daten']['kfzmodelldaten']:
        #print model
        if model['value'] =="" : continue
        data.append({'id':id, 'title': model['bez'], 'parent_id':parent_id, 'site_id':model['value'] })
        id+=1
    scraperwiki.sqlite.save(unique_keys=['id'], data=data, table_name="data");
