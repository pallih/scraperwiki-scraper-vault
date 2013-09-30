import scraperwiki
import urllib2
import lxml.etree
from lxml.builder import E

# TODO: does this need to be generalized for any URL or something?

url = "http://www.minneapolismn.gov/www/groups/public/@regservices/documents/webcontent/convert_254314.pdf" 
pdfdata = urllib2.urlopen(url).read()
# print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
#print "After converting to xml it has %d bytes" % len(xmldata)
#print xmldata
root = lxml.etree.fromstring(xmldata)

text_xpath = './/text'
find_xpath = root.findall(text_xpath)

in_entry = False
curr_entry = {}
entries = []

# Idea here is to just collect all the attributes, and then create
# individual elements for everything later-- i think lxml doesn't let
# you actually wrap an element or insert a begin at some point

# [{'ward': '01'}, {'ward': '01', 'vbr_date': '9/11/2008', 'address': '2830 POLK ST NE'}, ... ]

for line in find_xpath:
    # One attribute per line, and we want to trigger a new entry after
    # the address attribute

    new_entry, field_name = False, False

    if line.attrib['left'] == '618':
        field_name = 'ward'

    elif line.attrib['left'] == '667':
        field_name = 'neighborhood'

    elif line.attrib['left'] == '100':
        field_name = 'address'
        new_entry = True

    elif '296' < line.attrib['left'] < '312':
        field_name = 'vbr_date'

    elif '377' < line.attrib['left'] < '392':
        field_name = 'conb_date'

    elif '458' < line.attrib['left'] < '473':
        field_name = 'con1_date'

    elif '544' < line.attrib['left'] < '559':
        field_name = 'dirord_date'

    # Remove field from headers
    bad_fields = ["VBR ", "Date", "CON1 "]
    if line.text in bad_fields:
        field_name = False

        # Otherwise, if there's a field name that is not in bad_fields
    if field_name:
        curr_entry[field_name] = line.text
    if new_entry:
        # Address line has arrived, so if values have been set, append
        # to entry list, and then start a new entry
        if len(curr_entry.keys()) > 0:
            entries.append(curr_entry)
        curr_entry = {}


entry_nodes = []

all_keys = set()
for e in entries:
    # Collect all the keys and values from dictionary into individual nodes
    subnodes = [E(tag, text) for tag, text in e.iteritems()]
    for k in e.keys():
        all_keys.add(k)

    # make a house node containing all these
    house = E.house(*subnodes)
    entry_nodes.append(house)

all_the_houses = E.houses(*entry_nodes)

def to_array(house):
    """ Convert element into dict using every key in with all_keys
    """
    def maybe_get_text(key):
        try:
            return house.find(key).text
        except:
            return ''
    return map(maybe_get_text, all_keys)

# Converting elements to dictionaries, which means can probably remove the part about making new xml above, 
# scraperwiki.sqlite didn't seem to want to act on etree xml Node classes

house_dicts = []

for house in all_the_houses:
    array_values = to_array(house)
    house_dicts.append(dict(zip(all_keys, array_values)))

for house in house_dicts:
    scraperwiki.sqlite.save(unique_keys=['address'], 
                            data=house)
import scraperwiki
import urllib2
import lxml.etree
from lxml.builder import E

# TODO: does this need to be generalized for any URL or something?

url = "http://www.minneapolismn.gov/www/groups/public/@regservices/documents/webcontent/convert_254314.pdf" 
pdfdata = urllib2.urlopen(url).read()
# print "The pdf file has %d bytes" % len(pdfdata)

xmldata = scraperwiki.pdftoxml(pdfdata)
#print "After converting to xml it has %d bytes" % len(xmldata)
#print xmldata
root = lxml.etree.fromstring(xmldata)

text_xpath = './/text'
find_xpath = root.findall(text_xpath)

in_entry = False
curr_entry = {}
entries = []

# Idea here is to just collect all the attributes, and then create
# individual elements for everything later-- i think lxml doesn't let
# you actually wrap an element or insert a begin at some point

# [{'ward': '01'}, {'ward': '01', 'vbr_date': '9/11/2008', 'address': '2830 POLK ST NE'}, ... ]

for line in find_xpath:
    # One attribute per line, and we want to trigger a new entry after
    # the address attribute

    new_entry, field_name = False, False

    if line.attrib['left'] == '618':
        field_name = 'ward'

    elif line.attrib['left'] == '667':
        field_name = 'neighborhood'

    elif line.attrib['left'] == '100':
        field_name = 'address'
        new_entry = True

    elif '296' < line.attrib['left'] < '312':
        field_name = 'vbr_date'

    elif '377' < line.attrib['left'] < '392':
        field_name = 'conb_date'

    elif '458' < line.attrib['left'] < '473':
        field_name = 'con1_date'

    elif '544' < line.attrib['left'] < '559':
        field_name = 'dirord_date'

    # Remove field from headers
    bad_fields = ["VBR ", "Date", "CON1 "]
    if line.text in bad_fields:
        field_name = False

        # Otherwise, if there's a field name that is not in bad_fields
    if field_name:
        curr_entry[field_name] = line.text
    if new_entry:
        # Address line has arrived, so if values have been set, append
        # to entry list, and then start a new entry
        if len(curr_entry.keys()) > 0:
            entries.append(curr_entry)
        curr_entry = {}


entry_nodes = []

all_keys = set()
for e in entries:
    # Collect all the keys and values from dictionary into individual nodes
    subnodes = [E(tag, text) for tag, text in e.iteritems()]
    for k in e.keys():
        all_keys.add(k)

    # make a house node containing all these
    house = E.house(*subnodes)
    entry_nodes.append(house)

all_the_houses = E.houses(*entry_nodes)

def to_array(house):
    """ Convert element into dict using every key in with all_keys
    """
    def maybe_get_text(key):
        try:
            return house.find(key).text
        except:
            return ''
    return map(maybe_get_text, all_keys)

# Converting elements to dictionaries, which means can probably remove the part about making new xml above, 
# scraperwiki.sqlite didn't seem to want to act on etree xml Node classes

house_dicts = []

for house in all_the_houses:
    array_values = to_array(house)
    house_dicts.append(dict(zip(all_keys, array_values)))

for house in house_dicts:
    scraperwiki.sqlite.save(unique_keys=['address'], 
                            data=house)
