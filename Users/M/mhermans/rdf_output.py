# Generates basic corporation info in RDF
# Ontology cf. http://xmlns.com/foaf/corp/

from rdflib import Graph, URIRef, RDF, Literal, Namespace
from scraperwiki.apiwrapper import getKeys, getData
import scraperwiki

sourcescraper = "be_company_numbers"
scraperwiki.sqlite.attach(sourcescraper)
 
g = Graph()
CORP = Namespace('http://xmlns.com/foaf/corp#')

limit = 20
offset = 43000
query = '* from `be_company_numbers`.swdata LIMIT %s OFFSET %s' % (limit, offset) 

for row in scraperwiki.sqlite.select(query):
    #company_URI = URIRef('http://scraperwiki.com/resource/%s/%s' % (sourcescraper,row['ondnr'].replace('.','')))
    company_URI = URIRef('http://opencorporates.com/id/companies/be/%s' % (row['ondnr'].replace('.','')))
    g.add((company_URI, RDF.type, CORP.Company))
    for k, v in row.items():
        company_property = URIRef(CORP[k])
        value = Literal(v)
        g.add((company_URI, company_property, value))
        

print g.serialize(format='pretty-xml', indent="yes") # rdf/xml
#g.serialize(format='turtle')
# Generates basic corporation info in RDF
# Ontology cf. http://xmlns.com/foaf/corp/

from rdflib import Graph, URIRef, RDF, Literal, Namespace
from scraperwiki.apiwrapper import getKeys, getData
import scraperwiki

sourcescraper = "be_company_numbers"
scraperwiki.sqlite.attach(sourcescraper)
 
g = Graph()
CORP = Namespace('http://xmlns.com/foaf/corp#')

limit = 20
offset = 43000
query = '* from `be_company_numbers`.swdata LIMIT %s OFFSET %s' % (limit, offset) 

for row in scraperwiki.sqlite.select(query):
    #company_URI = URIRef('http://scraperwiki.com/resource/%s/%s' % (sourcescraper,row['ondnr'].replace('.','')))
    company_URI = URIRef('http://opencorporates.com/id/companies/be/%s' % (row['ondnr'].replace('.','')))
    g.add((company_URI, RDF.type, CORP.Company))
    for k, v in row.items():
        company_property = URIRef(CORP[k])
        value = Literal(v)
        g.add((company_URI, company_property, value))
        

print g.serialize(format='pretty-xml', indent="yes") # rdf/xml
#g.serialize(format='turtle')
