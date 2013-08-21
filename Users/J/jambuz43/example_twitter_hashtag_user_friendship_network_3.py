#gexf from google spreadsheet, picking up on http://mashe.hawksey.info/2011/12/google-plus-network-info-to-nodexl

import scraperwiki
import csv,urllib
import networkx as nx

#key='0AqGkLMU9sHmLdGNuQTdJWkJiQlQ5a21aclpBNmZQZnc'

#--via @mhawksey
# query string crib https://views.scraperwiki.com/run/python_querystring_cheat_sheet/?
#my defensive tweaks
import cgi, os
qstring=os.getenv("#ReplacetaglinewithJokowi")
if qstring!=None:
    get = dict(cgi.parse_qsl(qstring))
    if 'key' in get:
        key=get['key']
else:
    key=''
#---

stub='https://docs.google.com/spreadsheet/pub?key='+key+'&single=true&output=csv&gid='
nodesurl=stub+'1'
edgesurl=stub+'0'

nodesfile=urllib.urlopen(nodesurl)

DG=nx.DiGraph()

#utilities https://scraperwiki.com/scrapers/utility_library/
def vstr(s):
    if s:
        try:
            return unicode(s)
        except UnicodeDecodeError:
            return str(s)
    else:
        return u''
# remove any non ascii characters
def ascii(s): return "".join(i for i in s if ord(i)<128)
#===

#need to get rid of first row before the proper header row...
nodesfile.next()

nReader = csv.DictReader(nodesfile)
for nrow in nReader:
    #print nrow
    if nrow['ImageUrl']!=None:
        imgurl=nrow['ImageUrl']
    else: imgurl=''
    DG.add_node(nrow['Vertex'],label=ascii(nrow['Label']),name=ascii(nrow['Label']),imgurl=imgurl)

edgesfile=urllib.urlopen(edgesurl)
edgesfile.next()
eReader = csv.DictReader(edgesfile)
for erow in eReader:
    #print erow
    DG.add_edge(erow['Vertex 1'],erow['Vertex 2'])


import networkx.readwrite.gexf as gf

writer=gf.GEXFWriter(encoding='utf-8',prettyprint=True,version='1.1draft')
writer.add_graph(DG)

scraperwiki.utils.httpresponseheader("Content-Type", "text/xml")

from xml.etree.cElementTree import tostring
print tostring(writer.xml)