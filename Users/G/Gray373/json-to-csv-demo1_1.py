import scraperwiki
import json

from collections import OrderedDict

jsony_one="""[{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"},{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"}]"""

jsony_two="""[[{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"},{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"}],[{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"},{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"}],[{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"},{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"}],[],[{"a":"b"}]]"""

keylist=set() # records the names of sub-categories 

def getname(base, i):
    if type(i)==int:
        return "%s_%02d"%(base, i)
    else:
        return "%s_%s"%(base, i)

def unjson(name, json_text):
    j=json.loads(json_text)
    return uniterable(name, j)

def uniterable(name, iter):
    # given a single json fragment, convert it into a list of dicts suitable for importing into CSV.
    # name is the SQL name
    try:
        x=iter.keys()
    except AttributeError: # not a dict
        x=range(len(iter))
    out=dict()
    for i in x:
        succeed=False
        if type(iter[i]) in [list, dict, OrderedDict]:
            #looks jsony.
            try:
                r=uniterable(getname(name,i), iter[i]) # may not work
                out.update(r)
                succeed=True
            except:
                raise # should be pass, but refine 'except'
        if not succeed:
            out[getname(name,i)] = iter[i]
    return out

#print unjson('cat', jsony_one)


# make keylist
for item in json.loads(jsony_two):
    l=uniterable('cat', item)
    keylist.update(l.keys())

d={x:None for x in keylist}

# build dataset
for item in json.loads(jsony_two):
    l=dict(d)
    l.update(uniterable('cat', item))
    print l

import scraperwiki
import json

from collections import OrderedDict

jsony_one="""[{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"},{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"}]"""

jsony_two="""[[{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"},{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"}],[{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"},{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"}],[{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"},{"crumburl":"/", "name":"Home"},{"crumburl":"/Consultations", "name":"Consultations"},{"crumburl":null, "name":"Call for evidence - Review of Offender Learning"}],[],[{"a":"b"}]]"""

keylist=set() # records the names of sub-categories 

def getname(base, i):
    if type(i)==int:
        return "%s_%02d"%(base, i)
    else:
        return "%s_%s"%(base, i)

def unjson(name, json_text):
    j=json.loads(json_text)
    return uniterable(name, j)

def uniterable(name, iter):
    # given a single json fragment, convert it into a list of dicts suitable for importing into CSV.
    # name is the SQL name
    try:
        x=iter.keys()
    except AttributeError: # not a dict
        x=range(len(iter))
    out=dict()
    for i in x:
        succeed=False
        if type(iter[i]) in [list, dict, OrderedDict]:
            #looks jsony.
            try:
                r=uniterable(getname(name,i), iter[i]) # may not work
                out.update(r)
                succeed=True
            except:
                raise # should be pass, but refine 'except'
        if not succeed:
            out[getname(name,i)] = iter[i]
    return out

#print unjson('cat', jsony_one)


# make keylist
for item in json.loads(jsony_two):
    l=uniterable('cat', item)
    keylist.update(l.keys())

d={x:None for x in keylist}

# build dataset
for item in json.loads(jsony_two):
    l=dict(d)
    l.update(uniterable('cat', item))
    print l

