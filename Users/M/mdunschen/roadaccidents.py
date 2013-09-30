import scraperwiki
import xlrd
import csv

import urllib2
from zipfile import ZipFile
import cStringIO

import json

# url of keys
keysurl = "http://seagrass.goatchurch.org.uk/~martin/cgi-bin/uploads/Transparency_Export_Variables.xls"

# accidents url
accidents = "http://seagrass.goatchurch.org.uk/~martin/cgi-bin/uploads/Transparency_Acc_2010.csv"
casualties = "http://seagrass.goatchurch.org.uk/~martin/cgi-bin/uploads/Transparency_Cas_2010.zip" # not zip but csv
vehicles = "http://seagrass.goatchurch.org.uk/~martin/cgi-bin/uploads/Transparency_Veh_2010.zip" # not zip but csv 

knownmap = {"Pedestrian Crossing-Human Control"       : u"Ped Cross - Human",
            "Pedestrian Crossing-Physical Facilities" : u"Ped Cross - Physical",
            "Weather Conditions"                      : u"Weather",
            "Road Surface Conditions"                 : u"Road Surface",
            "Urban or Rural Area"                     : u"Urban Rural",
            "Did Police Officer Attend Scene of Accident" : u"Police Officer Attend",
            "Vehicle Location-Restricted Lane"        : u"Vehicle Location",
            "Vehicle Leaving Carriageway"             : u"Veh Leaving Carriageway",
            "Hit Object off Carriageway"              : u"Hit Object Off Carriageway",
            "Foreign Registered Vehicle"              : u"Foreign Registered Veh",
            "Journey Purpose of Driver"               : u"Journey Purpose",
            "Age Band of Driver"                      : u"Age Band",
            "Propulsion Code"                         : u"Vehicle Propulsion Code",
            "Age Band of Casualty"                    : u"Age Band",
            "Pedestrian Location"                     : u"Ped Location",
            "Pedestrian Movement"                     : u"Ped Movement",
            "Bus or Coach Passenger"                  : u"Bus Passenger",
            "Pedestrian Injured at Work"              : u"Ped Injured at Work",
            "Casualty IMD Decile"                     : u"IMD Decile",
            }


    # might be interesting to put these lookup tables into some database table and look them up from there
def readKeys():
    f = urllib2.urlopen(keysurl).read()
    wb = xlrd.open_workbook(file_contents=f)

    sheets = { }
    
    for s in wb.sheets():
        sheets[s.name] = { }
        # only interested in 2 column sheets
        if s.ncols == 2:
            for row in range(s.nrows):
                try:
                    sheets[s.name][int(s.cell(row,0).value)] = s.cell(row,1).value
                except ValueError:
                    pass

    return sheets

    # appears to make a transpose of the input table (is it transposed a second time before saving?)
def readSTATS19csv(url, ids):
    rows = list(csv.reader(urllib2.urlopen(url).readlines()))
    stdict = { }
    colnames = rows[0]
    for v in colnames:
        stdict[colnames.index(v)] = [ ]
    assert colnames[0] in ["Acc_Index", "Accident_Index"]
    for ls in rows[1:]:   # all rows.  slice later
        assert len(ls) == len(stdict)
        if not ids or ls[0] in ids:
            for i in xrange(len(ls)):
                stdict[i].append(ls[i])
    return stdict, colnames

def sliceSTATS19csv(ifrom, ito, stdict):
    rstdict = { }
    for i in range(len(stdict)):
        print i
        rstdict[i] = stdict[i][ifrom:ito]
    return rstdict


def findinlookup(cn, lookup): 
    global knownmap
    inum = cn.find('NUM')
    if inum != -1:
        cn = cn[:inum-1]
    v = cn.replace('_', ' ').strip()

    if unicode(v) in lookup:
        return lookup[unicode(v)]
    if v in knownmap:
        return lookup[unicode(knownmap[v])]
        


def savetodatastore(tablename, uniques, odict, colnames, lookup):
    nrecords = len(odict[0])
    chunk = 500
    ifrom = 0
    colnamelookup = { }
    for n in colnames:
        colnamelookup[n] = (findinlookup(n, lookup), cleanup(n))
    nsaved = 0
    while ifrom < nrecords:
        # build the dict to go into datastore
        d = []
        for i in range(ifrom, min(len(odict[0]), ifrom + chunk)):
            dl = dict([(cleanup(colnames[v]), odict[v][i] and odict[v][i].strip()) for v in range(len(odict.keys()))])
            for n in colnames:
                l, cleann = colnamelookup[n]
                if l:
                    if dl[cleann] != None:
                        m = int(dl[cleann])
                        if m in l:
                            dl["%s VALUE" % cleann] = l[m]
                        else:
                            #print "No value for: ", m,  " in: ", l
                            dl["%s VALUE" % cleann] = " "
                else:
                    pass
                    #print "Not found: ", n, lookup.keys()
            d.append(dl)                    
                                
        scraperwiki.sqlite.save(uniques, d, table_name=tablename)
        nsaved += len(d)
        ifrom += chunk
    assert nsaved == nrecords



def cleanup(colname):
    # replaces brackets that  sqlite does not like
    return colname.replace('(','').replace(')','').replace('\n','').replace('\r','').strip()

    
def scrape(ifrom=0):
    print "Reading from: ", ifrom
    s = readKeys()
    for t in knownmap.values():
        assert t in s

    chunk = 2500

    # read all the files once!
    laccdict, accnames = readSTATS19csv(accidents, [])


    # read accidents first, should have unique Accident indices
    while True:
        accdict = sliceSTATS19csv(ifrom, ifrom + chunk, laccdict)
        vehdict, vehnames = readSTATS19csv(vehicles, accdict[0])      
        casdict, casnames = readSTATS19csv(casualties, accdict[0])
        if not accdict[0]: # no more
            break
        print "Accidents: ", len(accdict[0])
        print "Vehicles: ", len(vehdict[0])
        print "Casualties: ", len(casdict[0])

        assert len(accdict.keys()) == len(accnames)
        savetodatastore("RoadAccidents2010 Accidents", [accnames[0]], accdict, accnames, s)
        savetodatastore("RoadAccidents2010 Vehicles", [vehnames[0], vehnames[1]], vehdict, vehnames, s) 
        savetodatastore("RoadAccidents2010 Casualties", [casnames[0], casnames[1], casnames[2]], casdict, casnames, s)  
        print "read to: ", ifrom + chunk
        ifrom += chunk
    del laccdict

def main():
    n = scraperwiki.sqlite.select("count(*) as c from `RoadAccidents2010 Accidents`")[0]["c"]
    scrape(n)

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)] 

#accdict, accnames = readSTATS19csv(accidents, 0, -1, []) 
#assert len(accdict[0]) == len(f7(accdict[0]))


main()import scraperwiki
import xlrd
import csv

import urllib2
from zipfile import ZipFile
import cStringIO

import json

# url of keys
keysurl = "http://seagrass.goatchurch.org.uk/~martin/cgi-bin/uploads/Transparency_Export_Variables.xls"

# accidents url
accidents = "http://seagrass.goatchurch.org.uk/~martin/cgi-bin/uploads/Transparency_Acc_2010.csv"
casualties = "http://seagrass.goatchurch.org.uk/~martin/cgi-bin/uploads/Transparency_Cas_2010.zip" # not zip but csv
vehicles = "http://seagrass.goatchurch.org.uk/~martin/cgi-bin/uploads/Transparency_Veh_2010.zip" # not zip but csv 

knownmap = {"Pedestrian Crossing-Human Control"       : u"Ped Cross - Human",
            "Pedestrian Crossing-Physical Facilities" : u"Ped Cross - Physical",
            "Weather Conditions"                      : u"Weather",
            "Road Surface Conditions"                 : u"Road Surface",
            "Urban or Rural Area"                     : u"Urban Rural",
            "Did Police Officer Attend Scene of Accident" : u"Police Officer Attend",
            "Vehicle Location-Restricted Lane"        : u"Vehicle Location",
            "Vehicle Leaving Carriageway"             : u"Veh Leaving Carriageway",
            "Hit Object off Carriageway"              : u"Hit Object Off Carriageway",
            "Foreign Registered Vehicle"              : u"Foreign Registered Veh",
            "Journey Purpose of Driver"               : u"Journey Purpose",
            "Age Band of Driver"                      : u"Age Band",
            "Propulsion Code"                         : u"Vehicle Propulsion Code",
            "Age Band of Casualty"                    : u"Age Band",
            "Pedestrian Location"                     : u"Ped Location",
            "Pedestrian Movement"                     : u"Ped Movement",
            "Bus or Coach Passenger"                  : u"Bus Passenger",
            "Pedestrian Injured at Work"              : u"Ped Injured at Work",
            "Casualty IMD Decile"                     : u"IMD Decile",
            }


    # might be interesting to put these lookup tables into some database table and look them up from there
def readKeys():
    f = urllib2.urlopen(keysurl).read()
    wb = xlrd.open_workbook(file_contents=f)

    sheets = { }
    
    for s in wb.sheets():
        sheets[s.name] = { }
        # only interested in 2 column sheets
        if s.ncols == 2:
            for row in range(s.nrows):
                try:
                    sheets[s.name][int(s.cell(row,0).value)] = s.cell(row,1).value
                except ValueError:
                    pass

    return sheets

    # appears to make a transpose of the input table (is it transposed a second time before saving?)
def readSTATS19csv(url, ids):
    rows = list(csv.reader(urllib2.urlopen(url).readlines()))
    stdict = { }
    colnames = rows[0]
    for v in colnames:
        stdict[colnames.index(v)] = [ ]
    assert colnames[0] in ["Acc_Index", "Accident_Index"]
    for ls in rows[1:]:   # all rows.  slice later
        assert len(ls) == len(stdict)
        if not ids or ls[0] in ids:
            for i in xrange(len(ls)):
                stdict[i].append(ls[i])
    return stdict, colnames

def sliceSTATS19csv(ifrom, ito, stdict):
    rstdict = { }
    for i in range(len(stdict)):
        print i
        rstdict[i] = stdict[i][ifrom:ito]
    return rstdict


def findinlookup(cn, lookup): 
    global knownmap
    inum = cn.find('NUM')
    if inum != -1:
        cn = cn[:inum-1]
    v = cn.replace('_', ' ').strip()

    if unicode(v) in lookup:
        return lookup[unicode(v)]
    if v in knownmap:
        return lookup[unicode(knownmap[v])]
        


def savetodatastore(tablename, uniques, odict, colnames, lookup):
    nrecords = len(odict[0])
    chunk = 500
    ifrom = 0
    colnamelookup = { }
    for n in colnames:
        colnamelookup[n] = (findinlookup(n, lookup), cleanup(n))
    nsaved = 0
    while ifrom < nrecords:
        # build the dict to go into datastore
        d = []
        for i in range(ifrom, min(len(odict[0]), ifrom + chunk)):
            dl = dict([(cleanup(colnames[v]), odict[v][i] and odict[v][i].strip()) for v in range(len(odict.keys()))])
            for n in colnames:
                l, cleann = colnamelookup[n]
                if l:
                    if dl[cleann] != None:
                        m = int(dl[cleann])
                        if m in l:
                            dl["%s VALUE" % cleann] = l[m]
                        else:
                            #print "No value for: ", m,  " in: ", l
                            dl["%s VALUE" % cleann] = " "
                else:
                    pass
                    #print "Not found: ", n, lookup.keys()
            d.append(dl)                    
                                
        scraperwiki.sqlite.save(uniques, d, table_name=tablename)
        nsaved += len(d)
        ifrom += chunk
    assert nsaved == nrecords



def cleanup(colname):
    # replaces brackets that  sqlite does not like
    return colname.replace('(','').replace(')','').replace('\n','').replace('\r','').strip()

    
def scrape(ifrom=0):
    print "Reading from: ", ifrom
    s = readKeys()
    for t in knownmap.values():
        assert t in s

    chunk = 2500

    # read all the files once!
    laccdict, accnames = readSTATS19csv(accidents, [])


    # read accidents first, should have unique Accident indices
    while True:
        accdict = sliceSTATS19csv(ifrom, ifrom + chunk, laccdict)
        vehdict, vehnames = readSTATS19csv(vehicles, accdict[0])      
        casdict, casnames = readSTATS19csv(casualties, accdict[0])
        if not accdict[0]: # no more
            break
        print "Accidents: ", len(accdict[0])
        print "Vehicles: ", len(vehdict[0])
        print "Casualties: ", len(casdict[0])

        assert len(accdict.keys()) == len(accnames)
        savetodatastore("RoadAccidents2010 Accidents", [accnames[0]], accdict, accnames, s)
        savetodatastore("RoadAccidents2010 Vehicles", [vehnames[0], vehnames[1]], vehdict, vehnames, s) 
        savetodatastore("RoadAccidents2010 Casualties", [casnames[0], casnames[1], casnames[2]], casdict, casnames, s)  
        print "read to: ", ifrom + chunk
        ifrom += chunk
    del laccdict

def main():
    n = scraperwiki.sqlite.select("count(*) as c from `RoadAccidents2010 Accidents`")[0]["c"]
    scrape(n)

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)] 

#accdict, accnames = readSTATS19csv(accidents, 0, -1, []) 
#assert len(accdict[0]) == len(f7(accdict[0]))


main()