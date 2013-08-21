import scraperwiki
sourcescraper = 'spine_lci_data'
scraperwiki.sqlite.attach(sourcescraper)           
data = scraperwiki.sqlite.select("* from SPINE2")
scraperwiki.utils.httpresponseheader( "Content-Type", "text/xml")
print '<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:eco="http://ontology.earthster.org/eco/core#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"><rdf:Description rdf:about="http://footprinted.org/rdfspace/lca/1000kgPolypropylenePP62280870"><rdfs:type rdf:resource="http://ontology.earthster.org/eco/core#FootprintModel"/>'
for d in data:
    print "<eco:hasQuantity><eco:hasUnitOfMeasure></eco:hasUnitOfMeasure><eco:hasMagnitude>" + d["quantity"] + "</eco:hasMagnitude></eco:hasQuantity>";

print "</rdf:Description></rdf:RDF>"