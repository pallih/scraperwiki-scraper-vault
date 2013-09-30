import scraperwiki
import lxml.html
import networkx
import itertools
import re
from xml.etree.cElementTree import tostring
import networkx.readwrite.gexf as gf


# Blank Python
sourcescraper = ''

base="http://wiki.openoil.net/"

def get_root(url):
    return lxml.html.fromstring(scraperwiki.scrape(url))

def get_list(url,xp):
    root=get_root(url)
    return root.xpath(xp)

def get_companies():
    listurl="http://wiki.openoil.net/index.php?title=Category:IOCs"
    ce=get_list(listurl,"//div[5]/table/tr/td/ul/li/a")
    return [(i.text_content(),"%s%s"%(base,i.attrib["href"])) for i in ce]

def get_countries(company):
    url=company[1]
    name=company[0]
    categories=[i.text_content() for i in get_list(url,"//div[5]/div/span/a")]
    countries=itertools.ifilter(lambda x: not "IOCs" in x, categories)
    return [(name,i) for i in countries]

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")    
relations=reduce(lambda x,y: x+y,[get_countries(c) for c in get_companies()],[])

graph=networkx.Graph()
for (n1,n2) in relations:
    graph.add_edge(n1,n2)

writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(graph)
print tostring(writer.xml)



import scraperwiki
import lxml.html
import networkx
import itertools
import re
from xml.etree.cElementTree import tostring
import networkx.readwrite.gexf as gf


# Blank Python
sourcescraper = ''

base="http://wiki.openoil.net/"

def get_root(url):
    return lxml.html.fromstring(scraperwiki.scrape(url))

def get_list(url,xp):
    root=get_root(url)
    return root.xpath(xp)

def get_companies():
    listurl="http://wiki.openoil.net/index.php?title=Category:IOCs"
    ce=get_list(listurl,"//div[5]/table/tr/td/ul/li/a")
    return [(i.text_content(),"%s%s"%(base,i.attrib["href"])) for i in ce]

def get_countries(company):
    url=company[1]
    name=company[0]
    categories=[i.text_content() for i in get_list(url,"//div[5]/div/span/a")]
    countries=itertools.ifilter(lambda x: not "IOCs" in x, categories)
    return [(name,i) for i in countries]

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")    
relations=reduce(lambda x,y: x+y,[get_countries(c) for c in get_companies()],[])

graph=networkx.Graph()
for (n1,n2) in relations:
    graph.add_edge(n1,n2)

writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(graph)
print tostring(writer.xml)



