import scraperwiki
import lxml.html

# from hausenblas / schema.org

schema_org_types = dict()


VOCAB_PREFIXES = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix vann: <http://purl.org/vocab/vann/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix sch: <http://schema.deri.ie/all#> .
"""


VOCAB_HEAD = """
<http://schema.deri.ie/all> a owl:Ontology;
    dc:title "Schema.org";
    dc:description "This is the RDF version of Schema.org";
    dc:modified "2011-06-03"^^xsd:date;
    vann:preferredNamespaceUri "http://schema.deri.ie/all#";
    vann:preferredNamespacePrefix "sch";
    foaf:page <http://schema.deri.ie/all.html> .
"""


########################
#  some helper functions


def dump_all_classes():
    global schema_org_types

    print VOCAB_PREFIXES
    print VOCAB_HEAD

    for t in schema_org_types:
        print "".join(["sch:", t, " a rdfs:Class, owl:Class ;"])
        print " rdfs:isDefinedBy <http://schema.deri.ie/all> ;"
        print "".join([" rdfs:label '", t, "' ."])


def dump_properties(of_class):
    global schema_org_types
    print VOCAB_PREFIXES
    print VOCAB_HEAD

    prop_list = schema_org_types[of_class]
    for p in prop_list:
        print "".join(["sch:", p, " a rdf:Property ;"])
        print " rdfs:isDefinedBy <http://schema.deri.ie/all> ;"
        print "".join([" rdfs:label '", p, "' ."])


# the incoming page has nexted <a> tags, which are illegal and automatically closed by lxml
# http://www.w3.org/TR/html401/struct/links.html#h-12.2.2
def main():
    global schema_org_types
    full_schema = scraperwiki.scrape("http://schema.org/docs/full.html")
    root = lxml.html.fromstring(full_schema)
    print lxml.html.tostring(root)

    # scrape the type definitions from schema.org and store them in the SQLite store
    for a in root.cssselect("div#mainContent a[name]"):
        atype = a.get('name')
        alink = a.getnext()
        assert alink.tag == "a" and alink.text == atype, lxml.html.tostring(alink)
        slot_list = [ ]
        stag = alink

            # scan forward from here to the next tag getting all the span.slot elements
        while True:
            stag = stag.getnext()
            if stag == None or stag.tag == "a":
                break
            if stag.tag == "br":
                continue
            assert stag.tag == "span" and stag.attrib.get("class") == "slot", lxml.html.tostring(stag)
            slot_list.append(stag.text)
        schema_org_types[atype] = slot_list
        print atype, slot_list
        #scraperwiki.sqlite.save(unique_keys=[atype], data=slot_list)


    # list the properties of a class
    #dump_properties('Thing')



main()import scraperwiki
import lxml.html

# from hausenblas / schema.org

schema_org_types = dict()


VOCAB_PREFIXES = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix dct: <http://purl.org/dc/terms/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix vann: <http://purl.org/vocab/vann/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix sch: <http://schema.deri.ie/all#> .
"""


VOCAB_HEAD = """
<http://schema.deri.ie/all> a owl:Ontology;
    dc:title "Schema.org";
    dc:description "This is the RDF version of Schema.org";
    dc:modified "2011-06-03"^^xsd:date;
    vann:preferredNamespaceUri "http://schema.deri.ie/all#";
    vann:preferredNamespacePrefix "sch";
    foaf:page <http://schema.deri.ie/all.html> .
"""


########################
#  some helper functions


def dump_all_classes():
    global schema_org_types

    print VOCAB_PREFIXES
    print VOCAB_HEAD

    for t in schema_org_types:
        print "".join(["sch:", t, " a rdfs:Class, owl:Class ;"])
        print " rdfs:isDefinedBy <http://schema.deri.ie/all> ;"
        print "".join([" rdfs:label '", t, "' ."])


def dump_properties(of_class):
    global schema_org_types
    print VOCAB_PREFIXES
    print VOCAB_HEAD

    prop_list = schema_org_types[of_class]
    for p in prop_list:
        print "".join(["sch:", p, " a rdf:Property ;"])
        print " rdfs:isDefinedBy <http://schema.deri.ie/all> ;"
        print "".join([" rdfs:label '", p, "' ."])


# the incoming page has nexted <a> tags, which are illegal and automatically closed by lxml
# http://www.w3.org/TR/html401/struct/links.html#h-12.2.2
def main():
    global schema_org_types
    full_schema = scraperwiki.scrape("http://schema.org/docs/full.html")
    root = lxml.html.fromstring(full_schema)
    print lxml.html.tostring(root)

    # scrape the type definitions from schema.org and store them in the SQLite store
    for a in root.cssselect("div#mainContent a[name]"):
        atype = a.get('name')
        alink = a.getnext()
        assert alink.tag == "a" and alink.text == atype, lxml.html.tostring(alink)
        slot_list = [ ]
        stag = alink

            # scan forward from here to the next tag getting all the span.slot elements
        while True:
            stag = stag.getnext()
            if stag == None or stag.tag == "a":
                break
            if stag.tag == "br":
                continue
            assert stag.tag == "span" and stag.attrib.get("class") == "slot", lxml.html.tostring(stag)
            slot_list.append(stag.text)
        schema_org_types[atype] = slot_list
        print atype, slot_list
        #scraperwiki.sqlite.save(unique_keys=[atype], data=slot_list)


    # list the properties of a class
    #dump_properties('Thing')



main()