##################################################################################
# This needs to be specialized to take account of the types and links of the different values
##################################################################################
from scraperwiki.apiwrapper import getKeys, getData
import StringIO
import re

sourcescraper = "incidenciesviaries_gencat"


# Issues:
# 1) Because it works as a look over the keys, this scraper is not very easy to customize for a particular scraper.  
#    Perhaps a list of keys should be one of the plastered in parameters, like sourcescraper

# 2) We don't have URIs for items in the database.  There was a method for looking up a single element in previous 
#    version by database-id.  Alternatively one could look up by unique keys and all sorts of things.  
#    It could be that generating the URI of every element is the hard bit that should take place in the scraper (maybe)

# 3) I don't know anything about RDF.  I have mimicked this output from that produced by dbpedia here.  
#    It is difficult to be enthusiastic without some live application that reads this data and does stuff with it.


limit = 20
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # alphabetically

out = StringIO.StringIO()
out.write('<?xml version="1.0" encoding="utf-8" ?>\n')
out.write('<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">\n')

mdomain = "http://scraperwiki.com/"
dtdomain = 'http://www.w3.org/2001/XMLSchema'


def WriteTriple(out, about, typ, k, v):
    out.write('<rdf:Description rdf:about="%s">\n' % about)
    out.write('    <swpprop:%s xmlns:swpprop="%s/property/" rdf:datatype="%s#%s">%s</swpprop:%s>\n' % (k, mdomain, dtdomain, typ, v, k))
    out.write('</rdf:Description>\n') 

wgs84d = 'xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#'
def WriteLatlng(out, about, lat, lng):
    out.write('<rdf:Description rdf:about="%s">\n' % about)
    out.write('    <geo:lat %s" rdf:datatype="http://www.w3.org/2001/XMLSchema#double">%s</geo:lat>' % (wgs84d, lat))
    out.write('</rdf:Description>\n') 
    out.write('<rdf:Description rdf:about="%s">\n' % about)
    out.write('    <geo:long %s" rdf:datatype="http://www.w3.org/2001/XMLSchema#double">%s</geo:long>' % (wgs84d, lng))
    out.write('</rdf:Description>\n') 

          
def gettype(v):
    try:
        int(v)
        return 'int'
    except ValueError:
        pass
              
    try:
        float(v)
        return 'double'
    except ValueError:
        pass

    if re.match('\d\d\d\d-\d\d-\d\d$', v):
        return 'date'
    return 'string'

              
for i, row in enumerate(getData(sourcescraper, limit, offset)):
    about = 'http://scraperwiki.com/resource/%s/%d' % (sourcescraper, i)

    for k, v in row.items():
        if not v:
            pass
        elif k == 'latlng':
            WriteLatlng(out, about, v[0], v[1])
        elif k == 'date':
            WriteTriple(out, about, 'date', k, v)
        else:
            WriteTriple(out, about, gettype(v), k, v)
out.write('</rdf:RDF>\n')
    
print out.getvalue()

##################################################################################
# This needs to be specialized to take account of the types and links of the different values
##################################################################################
from scraperwiki.apiwrapper import getKeys, getData
import StringIO
import re

sourcescraper = "incidenciesviaries_gencat"


# Issues:
# 1) Because it works as a look over the keys, this scraper is not very easy to customize for a particular scraper.  
#    Perhaps a list of keys should be one of the plastered in parameters, like sourcescraper

# 2) We don't have URIs for items in the database.  There was a method for looking up a single element in previous 
#    version by database-id.  Alternatively one could look up by unique keys and all sorts of things.  
#    It could be that generating the URI of every element is the hard bit that should take place in the scraper (maybe)

# 3) I don't know anything about RDF.  I have mimicked this output from that produced by dbpedia here.  
#    It is difficult to be enthusiastic without some live application that reads this data and does stuff with it.


limit = 20
offset = 0

keys = getKeys(sourcescraper)
keys.sort()  # alphabetically

out = StringIO.StringIO()
out.write('<?xml version="1.0" encoding="utf-8" ?>\n')
out.write('<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#">\n')

mdomain = "http://scraperwiki.com/"
dtdomain = 'http://www.w3.org/2001/XMLSchema'


def WriteTriple(out, about, typ, k, v):
    out.write('<rdf:Description rdf:about="%s">\n' % about)
    out.write('    <swpprop:%s xmlns:swpprop="%s/property/" rdf:datatype="%s#%s">%s</swpprop:%s>\n' % (k, mdomain, dtdomain, typ, v, k))
    out.write('</rdf:Description>\n') 

wgs84d = 'xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#'
def WriteLatlng(out, about, lat, lng):
    out.write('<rdf:Description rdf:about="%s">\n' % about)
    out.write('    <geo:lat %s" rdf:datatype="http://www.w3.org/2001/XMLSchema#double">%s</geo:lat>' % (wgs84d, lat))
    out.write('</rdf:Description>\n') 
    out.write('<rdf:Description rdf:about="%s">\n' % about)
    out.write('    <geo:long %s" rdf:datatype="http://www.w3.org/2001/XMLSchema#double">%s</geo:long>' % (wgs84d, lng))
    out.write('</rdf:Description>\n') 

          
def gettype(v):
    try:
        int(v)
        return 'int'
    except ValueError:
        pass
              
    try:
        float(v)
        return 'double'
    except ValueError:
        pass

    if re.match('\d\d\d\d-\d\d-\d\d$', v):
        return 'date'
    return 'string'

              
for i, row in enumerate(getData(sourcescraper, limit, offset)):
    about = 'http://scraperwiki.com/resource/%s/%d' % (sourcescraper, i)

    for k, v in row.items():
        if not v:
            pass
        elif k == 'latlng':
            WriteLatlng(out, about, v[0], v[1])
        elif k == 'date':
            WriteTriple(out, about, 'date', k, v)
        else:
            WriteTriple(out, about, gettype(v), k, v)
out.write('</rdf:RDF>\n')
    
print out.getvalue()

