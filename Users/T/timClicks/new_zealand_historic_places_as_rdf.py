import sys

from rdflib import Graph
from rdflib import Namespace, BNode, Literal, RDF, RDFS, URIRef
import scraperwiki

LIMIT = 100000


source = 'new_zealand_historic_places'
scraperwiki.sqlite.attach(source)



#common namespaces
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
DCMI = Namespace("http://purl.org/dc/dcmitype/")
VRA = Namespace('http://simile.mit.edu/2003/10/ontologies/vraCore3#')


NZHP = Namespace("http://www.historic.org.nz/TheRegister/RegisterSearch/RegisterResults.aspx?RID=")
#ad-hoc
HIS = Namespace("http://www.historic.org.nz/")

g = Graph()
g.bind('rdfs', RDFS)
g.bind('foaf', FOAF)
g.bind('dc', DC)
g.bind('dcmi', DCMI)
g.bind('dcterms', DCTERMS)
g.bind('reg', NZHP)
g.bind('hist', HIS)
g.bind('vra', VRA)

for p in scraperwiki.sqlite.select("* FROM new_zealand_historic_places.places LIMIT %s" % LIMIT):
    place = NZHP[str(p['place_id'])]
    g.add((place, RDF.type, HIS['place']))
    g.add((place, FOAF['page'], place))
    g.add((place, DC['title'], Literal(p['title'])))
    
    addy = p['address']
    if addy:
        g.add((place, HIS['address'], Literal(addy)))
        town = addy.split(',')[-1].strip() 
        if town.isupper():
            g.add((place, DC['coverage'], Literal(town.title())))
    if p['legal_description']:
         g.add((place, HIS['legal_description'], Literal(p['legal_description'])))
    if p['notable_features']:
        features = BNode()
        g.add((features, RDFS.label, Literal(p['notable_features'])))
        g.add((place, HIS['notable_features'], features))

for img in scraperwiki.sqlite.select("* FROM new_zealand_historic_places.images LIMIT %s" % LIMIT):
    place = NZHP[str(img['place_id'])]
    image = BNode()
    g.add((place, DCMI['Image'], image))
    g.add((image, DC['source'], URIRef(img['large_link'])))
    if img['caption']:
        g.add((image, DC['description'], Literal(img['caption'])))
    if img['photographer']:
        g.add((image, DC['creator'], Literal(img['photographer'])))
    if img['copyright']:
        g.add((image, DCTERMS['ProvenanceStatement'], Literal(img['copyright'])))

for use in scraperwiki.sqlite.select("* FROM new_zealand_historic_places.uses LIMIT %s" % LIMIT):
    place = NZHP[str(use['place_id'])]
    broad, narrow = use['use'].split(' - ', 1)
    u = BNode()
    g.add((u, HIS['use/category/broad'], Literal(broad)))
    g.add((u, HIS['use/category/narrow'], Literal(narrow)))
    g.add((u, HIS['use/type'], Literal(use['type'])))
    g.add((place, FOAF['topic'], Literal(broad)))
    g.add((place, FOAF['topic'], Literal(narrow)))    
    g.add((place, HIS['use'], u))

add = 'Addition'
mod = 'Modification'
oth = 'Other'
des = 'Designed'
orig = 'Original Construction'
thingsmap = {
"- Portico and dome completed.": mod,
"- Neon lights replaced": mod,
"- Maintenance work carried out": oth,
"- Site selected": des,
'- Entire building completed': orig,
"- Church consecrated and officially opened": oth,
"- New pipe organ installed": mod, 
"- Extensive maintenance work carried out; corrugated iron replaced": oth,
"- Second, possible construction date - site on which house rests purchased by Nannestad": orig,
"- Ground floor refurbished": mod,
"- Re-strengthening of the building": mod,
"- Restoration": mod,
"- Upper garden plot covered over with concrete": mod,
"- Repairs to Rocks Road Wall and chains": mod,
"- Lady chapel formed in south aisle. Alterations made to internal arches.": mod,
"- Maintenance carried out and plaque erected": oth,
"- Carillon restored": oth,
"- New clavier and practice clavier installed in Carillon": oth,
"- Restoration and repairs": oth,
"- Replacement of original drawing room fireplace.": mod,
"- Corrugated iron replaced shingles roof, some replacement of weather boards and studs, timber piles replaced by boulders.": oth,
"- Exterior plastered and foundations strengthened.": mod,
"- Additions to house the telephone exchange and mail.": add,
"- The front veranda, which was in a decayed condition and has been removed, will shortly be replicated.": mod,
"- Conversion to two flats, parts of north verandah enclosed (ground floor)": mod,
"- Renovations": mod,
"- Building repaired following fire damage": mod,
"- Main auditorium refurbished and enhanced": oth,
"- Cupola restored": oth,
"- Ship's wheel removed": mod,
"- vessel vandalised, beams from main deck stolen, weathering damage": mod,
"- Water system incorporated to prevent hull from drying out": mod,
"- Protective roof erected over hull": mod,
"- Chimneys demolished to roof level and ventilators removed from roof. Balcony from central first floor window fronting Oxford Street removed.": mod,
"- Security screens placed on ground floor windows and door on the Sumner Road frontage.": mod,
"- Removal of cupboards, one at end of central passage and two flanking range in kitchen, all unsympathetic later additions.": mod,
"- Removal into storage (on site) of the front door side lights and some ground floor doors. This was done to protect these features from possible damage by children, insertion of French doors in north elevation.": mod,
"- Internal modifications": mod,
"- The men's house portion of the homestead was modified. The kitchen was moved into one of the two rooms in this area of the homestead. The floors in part of the house have also been modified and laid in concrete.": mod,
"- New wall linings in keeping with the original on the other walls; wide opening made in north-western wall to form entry from new lobby, removal of plumbing fixtures.": mod,
"- Stables.": add,
'- Restoration and redevelopment': mod
}

for event in scraperwiki.sqlite.select("* FROM new_zealand_historic_places.events LIMIT %s" % LIMIT):
    typ = event['type']
    place = NZHP[str(event['place_id'])]
    evt = BNode()
    g.add((place, DCMI['Event'], evt))
    if typ == 'publication_written':
        g.add((place, DCTERMS['isReferencedBy'], evt))
        g.add((evt, DC['title'], Literal(event['description'])))
        g.add((evt, DC['created'], Literal(event['dates'])))
        g.add((evt, DC['description'], Literal(event['description'])))
    elif typ == 'construction':
        try:
            broad, narrow = event['description'].split(' - ', 1)
        except ValueError:
            desc = event['description'].strip()
            if desc  in set(['Original Construction', 'Relocation', 'Designed', 'Addition', 'Modification']):
                broad, narrow = desc, ''
            elif desc.startswith('- '):
                broad, narrow = thingsmap[desc], desc[2:]
            elif not desc:
                pass
            else:
                print desc
                raise
        if narrow:
            g.add((evt, RDFS.label, Literal(broad + ' - ' + narrow)))
        else:
            g.add((evt, RDFS.label, Literal(broad)))
        g.add((evt, DC['description'], Literal(narrow)))
        g.add((evt, DC['subject'], place))
        g.add((place, FOAF['topic'], Literal('Building ' + broad)))
        g.add((evt, HIS['event/category/broad'], Literal(broad)))
        g.add((evt, HIS['event/category/narrow'], Literal(narrow)))
        if event['date_orig'] is not None:
            try:
                orig = eval(event['date_orig'])
            except:
                # strings with random content raise all sorts of exceptions
                orig = event['date_orig']
        else:
            orig = "Unknown"
        evt_time = BNode()
        g.add((evt, DC['coverage'], evt_time))
        if event['is_range']:
            if isinstance(orig, list):
                orig = orig[0] + ' - ' + orig[1]
            g.add((evt_time, VRA['beginning'], Literal(event['date_range_start'])))
            g.add((evt_time, VRA['completion'], Literal(event['date_range_start'])))
            g.add((evt_time, DC['coverage'], Literal(orig)))
        else:
            g.add((evt_time, DC['date'], Literal(event['dates'])))
        if broad == 'Original Construction':
            g.add((place, DC['created'], evt_time))
            g.add((place, VRA['beginning'], evt_time))
        elif broad == 'Designed':
            g.add((place, VRA['design'], evt_time))
        elif 'restor' in narrow.lower() or 'repair' in narrow.lower():
            g.add((place, VRA['restoration'], evt_time))
        else:
            g.add((place, DC['modified'], evt_time))
            g.add((place, VRA['alteration'], evt_time))
    else:
        pass

# print len(g), sum(sys.getsizeof(n) for n in g.all_nodes())
print g.serialize(format='n3')

import sys

from rdflib import Graph
from rdflib import Namespace, BNode, Literal, RDF, RDFS, URIRef
import scraperwiki

LIMIT = 100000


source = 'new_zealand_historic_places'
scraperwiki.sqlite.attach(source)



#common namespaces
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
DCMI = Namespace("http://purl.org/dc/dcmitype/")
VRA = Namespace('http://simile.mit.edu/2003/10/ontologies/vraCore3#')


NZHP = Namespace("http://www.historic.org.nz/TheRegister/RegisterSearch/RegisterResults.aspx?RID=")
#ad-hoc
HIS = Namespace("http://www.historic.org.nz/")

g = Graph()
g.bind('rdfs', RDFS)
g.bind('foaf', FOAF)
g.bind('dc', DC)
g.bind('dcmi', DCMI)
g.bind('dcterms', DCTERMS)
g.bind('reg', NZHP)
g.bind('hist', HIS)
g.bind('vra', VRA)

for p in scraperwiki.sqlite.select("* FROM new_zealand_historic_places.places LIMIT %s" % LIMIT):
    place = NZHP[str(p['place_id'])]
    g.add((place, RDF.type, HIS['place']))
    g.add((place, FOAF['page'], place))
    g.add((place, DC['title'], Literal(p['title'])))
    
    addy = p['address']
    if addy:
        g.add((place, HIS['address'], Literal(addy)))
        town = addy.split(',')[-1].strip() 
        if town.isupper():
            g.add((place, DC['coverage'], Literal(town.title())))
    if p['legal_description']:
         g.add((place, HIS['legal_description'], Literal(p['legal_description'])))
    if p['notable_features']:
        features = BNode()
        g.add((features, RDFS.label, Literal(p['notable_features'])))
        g.add((place, HIS['notable_features'], features))

for img in scraperwiki.sqlite.select("* FROM new_zealand_historic_places.images LIMIT %s" % LIMIT):
    place = NZHP[str(img['place_id'])]
    image = BNode()
    g.add((place, DCMI['Image'], image))
    g.add((image, DC['source'], URIRef(img['large_link'])))
    if img['caption']:
        g.add((image, DC['description'], Literal(img['caption'])))
    if img['photographer']:
        g.add((image, DC['creator'], Literal(img['photographer'])))
    if img['copyright']:
        g.add((image, DCTERMS['ProvenanceStatement'], Literal(img['copyright'])))

for use in scraperwiki.sqlite.select("* FROM new_zealand_historic_places.uses LIMIT %s" % LIMIT):
    place = NZHP[str(use['place_id'])]
    broad, narrow = use['use'].split(' - ', 1)
    u = BNode()
    g.add((u, HIS['use/category/broad'], Literal(broad)))
    g.add((u, HIS['use/category/narrow'], Literal(narrow)))
    g.add((u, HIS['use/type'], Literal(use['type'])))
    g.add((place, FOAF['topic'], Literal(broad)))
    g.add((place, FOAF['topic'], Literal(narrow)))    
    g.add((place, HIS['use'], u))

add = 'Addition'
mod = 'Modification'
oth = 'Other'
des = 'Designed'
orig = 'Original Construction'
thingsmap = {
"- Portico and dome completed.": mod,
"- Neon lights replaced": mod,
"- Maintenance work carried out": oth,
"- Site selected": des,
'- Entire building completed': orig,
"- Church consecrated and officially opened": oth,
"- New pipe organ installed": mod, 
"- Extensive maintenance work carried out; corrugated iron replaced": oth,
"- Second, possible construction date - site on which house rests purchased by Nannestad": orig,
"- Ground floor refurbished": mod,
"- Re-strengthening of the building": mod,
"- Restoration": mod,
"- Upper garden plot covered over with concrete": mod,
"- Repairs to Rocks Road Wall and chains": mod,
"- Lady chapel formed in south aisle. Alterations made to internal arches.": mod,
"- Maintenance carried out and plaque erected": oth,
"- Carillon restored": oth,
"- New clavier and practice clavier installed in Carillon": oth,
"- Restoration and repairs": oth,
"- Replacement of original drawing room fireplace.": mod,
"- Corrugated iron replaced shingles roof, some replacement of weather boards and studs, timber piles replaced by boulders.": oth,
"- Exterior plastered and foundations strengthened.": mod,
"- Additions to house the telephone exchange and mail.": add,
"- The front veranda, which was in a decayed condition and has been removed, will shortly be replicated.": mod,
"- Conversion to two flats, parts of north verandah enclosed (ground floor)": mod,
"- Renovations": mod,
"- Building repaired following fire damage": mod,
"- Main auditorium refurbished and enhanced": oth,
"- Cupola restored": oth,
"- Ship's wheel removed": mod,
"- vessel vandalised, beams from main deck stolen, weathering damage": mod,
"- Water system incorporated to prevent hull from drying out": mod,
"- Protective roof erected over hull": mod,
"- Chimneys demolished to roof level and ventilators removed from roof. Balcony from central first floor window fronting Oxford Street removed.": mod,
"- Security screens placed on ground floor windows and door on the Sumner Road frontage.": mod,
"- Removal of cupboards, one at end of central passage and two flanking range in kitchen, all unsympathetic later additions.": mod,
"- Removal into storage (on site) of the front door side lights and some ground floor doors. This was done to protect these features from possible damage by children, insertion of French doors in north elevation.": mod,
"- Internal modifications": mod,
"- The men's house portion of the homestead was modified. The kitchen was moved into one of the two rooms in this area of the homestead. The floors in part of the house have also been modified and laid in concrete.": mod,
"- New wall linings in keeping with the original on the other walls; wide opening made in north-western wall to form entry from new lobby, removal of plumbing fixtures.": mod,
"- Stables.": add,
'- Restoration and redevelopment': mod
}

for event in scraperwiki.sqlite.select("* FROM new_zealand_historic_places.events LIMIT %s" % LIMIT):
    typ = event['type']
    place = NZHP[str(event['place_id'])]
    evt = BNode()
    g.add((place, DCMI['Event'], evt))
    if typ == 'publication_written':
        g.add((place, DCTERMS['isReferencedBy'], evt))
        g.add((evt, DC['title'], Literal(event['description'])))
        g.add((evt, DC['created'], Literal(event['dates'])))
        g.add((evt, DC['description'], Literal(event['description'])))
    elif typ == 'construction':
        try:
            broad, narrow = event['description'].split(' - ', 1)
        except ValueError:
            desc = event['description'].strip()
            if desc  in set(['Original Construction', 'Relocation', 'Designed', 'Addition', 'Modification']):
                broad, narrow = desc, ''
            elif desc.startswith('- '):
                broad, narrow = thingsmap[desc], desc[2:]
            elif not desc:
                pass
            else:
                print desc
                raise
        if narrow:
            g.add((evt, RDFS.label, Literal(broad + ' - ' + narrow)))
        else:
            g.add((evt, RDFS.label, Literal(broad)))
        g.add((evt, DC['description'], Literal(narrow)))
        g.add((evt, DC['subject'], place))
        g.add((place, FOAF['topic'], Literal('Building ' + broad)))
        g.add((evt, HIS['event/category/broad'], Literal(broad)))
        g.add((evt, HIS['event/category/narrow'], Literal(narrow)))
        if event['date_orig'] is not None:
            try:
                orig = eval(event['date_orig'])
            except:
                # strings with random content raise all sorts of exceptions
                orig = event['date_orig']
        else:
            orig = "Unknown"
        evt_time = BNode()
        g.add((evt, DC['coverage'], evt_time))
        if event['is_range']:
            if isinstance(orig, list):
                orig = orig[0] + ' - ' + orig[1]
            g.add((evt_time, VRA['beginning'], Literal(event['date_range_start'])))
            g.add((evt_time, VRA['completion'], Literal(event['date_range_start'])))
            g.add((evt_time, DC['coverage'], Literal(orig)))
        else:
            g.add((evt_time, DC['date'], Literal(event['dates'])))
        if broad == 'Original Construction':
            g.add((place, DC['created'], evt_time))
            g.add((place, VRA['beginning'], evt_time))
        elif broad == 'Designed':
            g.add((place, VRA['design'], evt_time))
        elif 'restor' in narrow.lower() or 'repair' in narrow.lower():
            g.add((place, VRA['restoration'], evt_time))
        else:
            g.add((place, DC['modified'], evt_time))
            g.add((place, VRA['alteration'], evt_time))
    else:
        pass

# print len(g), sum(sys.getsizeof(n) for n in g.all_nodes())
print g.serialize(format='n3')

