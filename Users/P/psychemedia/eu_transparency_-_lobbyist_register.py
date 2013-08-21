import scraperwiki
import mechanize

# http://ec.europa.eu/transparencyregister/public/consultation/statistics.do?locale=en&action=prepareView

#---
#via https://github.com/hay/xml2json/blob/master/xml2json.py
import xml.etree.cElementTree as ET
import simplejson

def elem_to_internal(elem,strip=1):

    """Convert an Element into an internal dictionary (not JSON!)."""

    d = {}
    for key, value in elem.attrib.items():
        d['@'+key] = value

    # loop over subelements to merge them
    for subelem in elem:
        v = elem_to_internal(subelem,strip=strip)
        tag = subelem.tag
        value = v[tag]
        try:
            # add to existing list for this tag
            d[tag].append(value)
        except AttributeError:
            # turn existing entry into a list
            d[tag] = [d[tag], value]
        except KeyError:
            # add a new non-list entry
            d[tag] = value
    text = elem.text
    tail = elem.tail
    if strip:
        # ignore leading and trailing whitespace
        if text: text = text.strip()
        if tail: tail = tail.strip()

    if tail:
        d['#tail'] = tail

    if d:
        # use #text element if other attributes exist
        if text: d["#text"] = text
    else:
        # text is the value if no attributes
        d = text or None
    return {elem.tag: d}


def internal_to_elem(pfsh, factory=ET.Element):

    """Convert an internal dictionary (not JSON!) into an Element.

    Whatever Element implementation we could import will be
    used by default; if you want to use something else, pass the
    Element class as the factory parameter.
    """

    attribs = {}
    text = None
    tail = None
    sublist = []
    tag = pfsh.keys()
    if len(tag) != 1:
        raise ValueError("Illegal structure with multiple tags: %s" % tag)
    tag = tag[0]
    value = pfsh[tag]
    if isinstance(value,dict):
        for k, v in value.items():
            if k[:1] == "@":
                attribs[k[1:]] = v
            elif k == "#text":
                text = v
            elif k == "#tail":
                tail = v
            elif isinstance(v, list):
                for v2 in v:
                    sublist.append(internal_to_elem({k:v2},factory=factory))
            else:
                sublist.append(internal_to_elem({k:v},factory=factory))
    else:
        text = value
    e = factory(tag, attribs)
    for sub in sublist:
        e.append(sub)
    e.text = text
    e.tail = tail
    return e


def elem2json(elem, strip=1):

    """Convert an ElementTree or Element into a JSON string."""

    if hasattr(elem, 'getroot'):
        elem = elem.getroot()
    return simplejson.dumps(elem_to_internal(elem,strip=strip))


def json2elem(json, factory=ET.Element):

    """Convert a JSON string into an Element.

    Whatever Element implementation we could import will be used by
    default; if you want to use something else, pass the Element class
    as the factory parameter.
    """

    return internal_to_elem(simplejson.loads(json), factory)


def xml2json(xmlstring,strip=1):

    """Convert an XML string into a JSON string."""

    elem = ET.fromstring(xmlstring)
    return elem2json(elem,strip=strip)


def json2xml(json, factory=ET.Element):

    """Convert a JSON string into an XML string.

    Whatever Element implementation we could import will be used by
    default; if you want to use something else, pass the Element class
    as the factory parameter.
    """

    elem = internal_to_elem(simplejson.loads(json), factory)
    return ET.tostring(elem)

#-----

print 'Grabbing XML file'
xmlURL='http://ec.europa.eu/transparencyregister/public/consultation/statistics.do?action=getLobbyistsXml&fileType=NEW'
#f=urllib.urlopen(xmlURL)
f = mechanize.urlopen(xmlURL)
xml=f.read()
f.close()
print '...grabbed'

print 'Convert to json str'
j=xml2json(xml)
print '...converted'

print 'replace namespace'
j=j.replace('{http://intragate.ec.europa.eu/transparencyregister/intws/20110715}','')
j=j.replace('@{http://www.w3.org/1999/xlink}','')
j=j.replace('@{http://www.w3.org/2001/XMLSchema-instance}','')
j=j.replace('@index','index')
j=j.replace('@currency','currency')
print '...replaced'

print 'Convert to json'
json=simplejson.loads(j)
print '...converted'

bigdata=[]
tn='mainData'
for i in json["ListOfIRPublicDetail"]["resultList"]['interestRepresentativeNew']:
    d={}
    d['id']=i['identificationCode']
    d['name']=i['name']['originalName']
    d['goals']=i['goals']
    d['category']=i['category']['mainCategory']
    d['activities']=i['activities']
    d['eurSourcesGrants']=i['financialData']['eurSourcesGrants']
    d['eurSourcesGrants']=i['financialData']['eurSourcesProcurement']
    if 'cost' in i['financialData']['financialInformation']:
        if 'absoluteAmount' in i['financialData']['financialInformation']['cost']:
            d['absoluteAmount']=i['financialData']['financialInformation']['cost']['absoluteAmount']
    bigdata.append(d.copy())
    if len(bigdata)>1000:
        scraperwiki.sqlite.save(unique_keys=['id'], table_name=tn, data=bigdata,verbose=0)
        bigdata=[]
scraperwiki.sqlite.save(unique_keys=['id'], table_name=tn, data=bigdata,verbose=0)