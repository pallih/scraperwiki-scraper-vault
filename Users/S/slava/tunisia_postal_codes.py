import scraperwiki
import lxml.html

# Blank Python

scraperwiki.sqlite.execute("delete from data")
html = scraperwiki.scrape("http://www.poste.tn/codes.php")
root = lxml.html.document_fromstring(html)
cities = root.xpath("//select[@name='ville']/option")
i=1
for city_el in cities:
    guvernorat_id=city_el.attrib['value']
    guvernorat_name=city_el.text_content()

    if guvernorat_id == '0': continue

    html = scraperwiki.scrape("http://www.poste.tn/codes_ajax.php", {'ville':guvernorat_id, 'do': 'delegation'})
    root1 = lxml.html.fromstring(html)
    delegation = root1.xpath("//select[@name='delegation']/option")
    print delegation
    for delegation_el in delegation:
        
        delegation_id = delegation_el.attrib['value']
        delegation_name = delegation_el.text_content()
        
        if delegation_id == '0':continue

        html = scraperwiki.scrape("http://www.poste.tn/codes_ajax.php", {'ville': guvernorat_id, 'delegation': delegation_id, 'do': 'localite'})
        root = lxml.html.fromstring(html)
        localite = root.xpath("//select[@name='localite']/option")

        for localite_el in localite:
            
            localite_id = localite_el.attrib['value']
            localite_name = localite_el.text_content()
            
            if localite_id == '0':continue
    
            html = scraperwiki.scrape("http://www.poste.tn/codes_ajax.php", {'ville': guvernorat_id, 'delegation': delegation_id, 'localite':localite_id, 'do': 'resultat'})
            root = lxml.html.fromstring(html)
            res = root.xpath("//table/tr[position()>4 and position()<last()]")
            for r in res:
                scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i, \
                    'guvernorate':r[0].text_content(), \
                    'delegation':r[1].text_content(), \
                    'localite': r[2].text_content(), \
                    'postal_code': r[3].text_content()}, table_name='data')
                i+=1

    
    