# Incomplete

# Generates basic corporation info in RDF
# Ontology cf. http://xmlns.com/foaf/corp/

from rdflib import Graph, URIRef, RDF, Literal, Namespace, BNode
from scraperwiki.apiwrapper import getKeys, getData
import scraperwiki
from elementtidy import TidyHTMLTreeBuilder


sourcescraper = 'members_club_van_lotharingen'
scraperwiki.sqlite.attach(sourcescraper)
 
g = Graph()
CORP = Namespace('http://xmlns.com/foaf/corp#')

limit = 20
offset = 43000

clubURI = URIRef('http://rdf.freebase.com/ns/en.cercle_de_lorraine')

for row in scraperwiki.sqlite.select('* from `%s`.swdata LIMIT %s OFFSET %s' % (sourcescraper, limit, offset) ):
    company_URI = URIRef('http://scraperwiki.com/resource/%s/%s' % (sourcescraper,row['ondnr'].replace('.','')))
    g.add((company_URI, RDF.type, CORP.Company))
    for k, v in row.items():
        company_property = URIRef(CORP[k])
        value = Literal(v)
        g.add((company_URI, company_property, value))
        

print g.serialize(format='pretty-xml', indent="yes") # rdf/xml
#g.serialize(format='turtle')

# Incomplete

# Generates basic corporation info in RDF
# Ontology cf. http://xmlns.com/foaf/corp/

from rdflib import Graph, URIRef, RDF, Literal, Namespace, BNode
from scraperwiki.apiwrapper import getKeys, getData
import scraperwiki
from elementtidy import TidyHTMLTreeBuilder


sourcescraper = 'members_club_van_lotharingen'
scraperwiki.sqlite.attach(sourcescraper)
 
g = Graph()
CORP = Namespace('http://xmlns.com/foaf/corp#')

limit = 20
offset = 43000

clubURI = URIRef('http://rdf.freebase.com/ns/en.cercle_de_lorraine')

for row in scraperwiki.sqlite.select('* from `%s`.swdata LIMIT %s OFFSET %s' % (sourcescraper, limit, offset) ):
    company_URI = URIRef('http://scraperwiki.com/resource/%s/%s' % (sourcescraper,row['ondnr'].replace('.','')))
    g.add((company_URI, RDF.type, CORP.Company))
    for k, v in row.items():
        company_property = URIRef(CORP[k])
        value = Literal(v)
        g.add((company_URI, company_property, value))
        

print g.serialize(format='pretty-xml', indent="yes") # rdf/xml
#g.serialize(format='turtle')

