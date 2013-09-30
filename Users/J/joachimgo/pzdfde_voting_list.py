import scraperwiki
import lxml.html

xml = scraperwiki.scrape("http://p.zdf.de/bt09/data_abst_liste.php") 
root = lxml.html.fromstring(xml)
map = {'Titel': 'title', 'Kurzzusammenfassung': 'description', 'Datum': 'pubDate', 'ID': 'guid'} #additional fields for RSS-API

for data in root.cssselect("data"): 
   d = {}
   for prop in data.cssselect("property"):      
      d[prop.attrib["name"]] = prop.text
      if prop.attrib["name"] in map:
        d[map[prop.attrib["name"]]] = prop.text;
   
   d['link'] = 'http://p.zdf.de/?abstID=' + d['ID'];
   scraperwiki.sqlite.save(unique_keys=['ID'], data=d)


xml = scraperwiki.scrape("http://p.zdf.de/bt09/data_abg_liste.php?period=17&orderby=sortName")
root = lxml.html.fromstring(xml)

for data in root.cssselect("data"): 
   d = {}
   for prop in data.cssselect("property"):      
      d[prop.attrib["name"]] = prop.text
   scraperwiki.sqlite.save(unique_keys=['ID'], data=d, table_name="swdata_abg")
import scraperwiki
import lxml.html

xml = scraperwiki.scrape("http://p.zdf.de/bt09/data_abst_liste.php") 
root = lxml.html.fromstring(xml)
map = {'Titel': 'title', 'Kurzzusammenfassung': 'description', 'Datum': 'pubDate', 'ID': 'guid'} #additional fields for RSS-API

for data in root.cssselect("data"): 
   d = {}
   for prop in data.cssselect("property"):      
      d[prop.attrib["name"]] = prop.text
      if prop.attrib["name"] in map:
        d[map[prop.attrib["name"]]] = prop.text;
   
   d['link'] = 'http://p.zdf.de/?abstID=' + d['ID'];
   scraperwiki.sqlite.save(unique_keys=['ID'], data=d)


xml = scraperwiki.scrape("http://p.zdf.de/bt09/data_abg_liste.php?period=17&orderby=sortName")
root = lxml.html.fromstring(xml)

for data in root.cssselect("data"): 
   d = {}
   for prop in data.cssselect("property"):      
      d[prop.attrib["name"]] = prop.text
   scraperwiki.sqlite.save(unique_keys=['ID'], data=d, table_name="swdata_abg")
