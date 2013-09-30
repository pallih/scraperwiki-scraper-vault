import scraperwiki
import lxml.html

def get_itis_taxonomy(tsn):
    taxon = []
    tsn = tsn
    html = scraperwiki.scrape('http://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value='+str(tsn))
    root = lxml.html.fromstring(html)
    trs = root.cssselect('tr')
    for tr in trs:
        if lxml.html.tostring(tr).find('Taxonomic Hierarchy')>0:
            tables = tr.cssselect('table')
    trs = tables[len(tables)-1].cssselect('tr')
    direct_children = 0
    for tr in trs:
        row = [] 
        if lxml.html.tostring(tr).find('Direct Children:')>0:
            direct_children=1
        if direct_children == 0:
            if lxml.html.tostring(tr).find('datafield')>0:
                tds = tr.cssselect('td')
                hrefs = tr.cssselect('a')
#                print tds[1].text.strip()
                row.append(tds[1].text.encode('ascii','ignore').strip())
                if len(hrefs)>0:
#                    print hrefs[0].text.strip()
                    row.append(hrefs[0].text.encode('ascii','ignore').strip())
                    taxon.append(row)
                else:
                    tds = tr.cssselect('td')
                    row.append(tds[2].text.encode('ascii','ignore').strip())
                    taxon.append(row)
                    return taxon

tsn = 180584
x = get_itis_taxonomy(tsn)

scraperwiki.sqlite.execute('DROP TABLE IF EXISTS itis_taxa')
scraperwiki.sqlite.execute('CREATE TABLE itis_taxa (`tsn` integer PRIMARY KEY, `Kingdom` text, `Phylum` text, `Subphylum` text, `Class` text, `Subclass` text, `Infraclass` text, `Order` text, `Suborder` text, `Family` text, `Subfamily` text, `Genus` text, `Species` text)')
scraperwiki.sqlite.execute('insert into itis_taxa (`tsn`) values ('+str(tsn)+');')
scraperwiki.sqlite.commit()
scraperwiki.sqlite.execute('update itis_taxa set `Kingdom` = \'Animalia\' where `tsn`='+str(tsn)+';')

for item in x:
    scraperwiki.sqlite.execute('update itis_taxa set `'+item[0]+'` = \''+item[1]+'\' where `tsn`='+str(tsn)+';')
    print item[0], item[1]

scraperwiki.sqlite.commit()
scraperwiki.sqlite.execute('select * from itis_taxa;')
print scraperwiki.sqlite.execute("select * from itis_taxa") 
#for eachList in x:
#    scraperwiki.sqlite.execute('update itis_taxa set `'+Kingdom+'` = '+Animalia+'\' where `tsn`='+str(tsn)+';')
#    print (eachList[])
#print (x[0][0])


import scraperwiki
import lxml.html

def get_itis_taxonomy(tsn):
    taxon = []
    tsn = tsn
    html = scraperwiki.scrape('http://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value='+str(tsn))
    root = lxml.html.fromstring(html)
    trs = root.cssselect('tr')
    for tr in trs:
        if lxml.html.tostring(tr).find('Taxonomic Hierarchy')>0:
            tables = tr.cssselect('table')
    trs = tables[len(tables)-1].cssselect('tr')
    direct_children = 0
    for tr in trs:
        row = [] 
        if lxml.html.tostring(tr).find('Direct Children:')>0:
            direct_children=1
        if direct_children == 0:
            if lxml.html.tostring(tr).find('datafield')>0:
                tds = tr.cssselect('td')
                hrefs = tr.cssselect('a')
#                print tds[1].text.strip()
                row.append(tds[1].text.encode('ascii','ignore').strip())
                if len(hrefs)>0:
#                    print hrefs[0].text.strip()
                    row.append(hrefs[0].text.encode('ascii','ignore').strip())
                    taxon.append(row)
                else:
                    tds = tr.cssselect('td')
                    row.append(tds[2].text.encode('ascii','ignore').strip())
                    taxon.append(row)
                    return taxon

tsn = 180584
x = get_itis_taxonomy(tsn)

scraperwiki.sqlite.execute('DROP TABLE IF EXISTS itis_taxa')
scraperwiki.sqlite.execute('CREATE TABLE itis_taxa (`tsn` integer PRIMARY KEY, `Kingdom` text, `Phylum` text, `Subphylum` text, `Class` text, `Subclass` text, `Infraclass` text, `Order` text, `Suborder` text, `Family` text, `Subfamily` text, `Genus` text, `Species` text)')
scraperwiki.sqlite.execute('insert into itis_taxa (`tsn`) values ('+str(tsn)+');')
scraperwiki.sqlite.commit()
scraperwiki.sqlite.execute('update itis_taxa set `Kingdom` = \'Animalia\' where `tsn`='+str(tsn)+';')

for item in x:
    scraperwiki.sqlite.execute('update itis_taxa set `'+item[0]+'` = \''+item[1]+'\' where `tsn`='+str(tsn)+';')
    print item[0], item[1]

scraperwiki.sqlite.commit()
scraperwiki.sqlite.execute('select * from itis_taxa;')
print scraperwiki.sqlite.execute("select * from itis_taxa") 
#for eachList in x:
#    scraperwiki.sqlite.execute('update itis_taxa set `'+Kingdom+'` = '+Animalia+'\' where `tsn`='+str(tsn)+';')
#    print (eachList[])
#print (x[0][0])


