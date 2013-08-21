import scraperwiki
import urllib

# Documentation for file standard:
#http://www.census.gov/geo/www/gazetteer/places2k_layout.html#counties

fin = urllib.urlopen("http://www.census.gov/tiger/tms/gazetteer/county2k.txt")

totallandareamsq = 0.0
totalwaterareamsq = 0.0

for line in fin.readlines():
    data = { }
    data["state"]               = line[0:2]
    data["FIPS state code"]     = line[2:4]
    data["FIPS county code"]    = line[4:7]
    data["county name"]         = unicode(line[7:71].strip(), "latin1")
    data["Total population"]    = int(line[71:80].strip())
    data["Total Housing Units"] = int(line[80:89].strip())
    data["Land area msq"]       = int(line[89:103].strip())
    data["Water area msq"]      = int(line[103:117].strip())
    latlng = [ float(line[141:151].strip()), float(line[151:162].strip()) ]
    scraperwiki.datastore.save(unique_keys=["FIPS state code", "FIPS county code"], data=data, latlng=latlng, silent=True)
    totallandareamsq += data["Land area msq"]
    totalwaterareamsq += data["Water area msq"]

print "Total land area=%.1f m^2, Total water area=%.1f m^2" % (totallandareamsq, totalwaterareamsq)

# (check why I need unicode(latin1) here as I thought I was trapping such exceptions 
# before they reached the JSON encoding stage)
import scraperwiki
import urllib

# Documentation for file standard:
#http://www.census.gov/geo/www/gazetteer/places2k_layout.html#counties

fin = urllib.urlopen("http://www.census.gov/tiger/tms/gazetteer/county2k.txt")

totallandareamsq = 0.0
totalwaterareamsq = 0.0

for line in fin.readlines():
    data = { }
    data["state"]               = line[0:2]
    data["FIPS state code"]     = line[2:4]
    data["FIPS county code"]    = line[4:7]
    data["county name"]         = unicode(line[7:71].strip(), "latin1")
    data["Total population"]    = int(line[71:80].strip())
    data["Total Housing Units"] = int(line[80:89].strip())
    data["Land area msq"]       = int(line[89:103].strip())
    data["Water area msq"]      = int(line[103:117].strip())
    latlng = [ float(line[141:151].strip()), float(line[151:162].strip()) ]
    scraperwiki.datastore.save(unique_keys=["FIPS state code", "FIPS county code"], data=data, latlng=latlng, silent=True)
    totallandareamsq += data["Land area msq"]
    totalwaterareamsq += data["Water area msq"]

print "Total land area=%.1f m^2, Total water area=%.1f m^2" % (totallandareamsq, totalwaterareamsq)

# (check why I need unicode(latin1) here as I thought I was trapping such exceptions 
# before they reached the JSON encoding stage)
import scraperwiki
import urllib

# Documentation for file standard:
#http://www.census.gov/geo/www/gazetteer/places2k_layout.html#counties

fin = urllib.urlopen("http://www.census.gov/tiger/tms/gazetteer/county2k.txt")

totallandareamsq = 0.0
totalwaterareamsq = 0.0

for line in fin.readlines():
    data = { }
    data["state"]               = line[0:2]
    data["FIPS state code"]     = line[2:4]
    data["FIPS county code"]    = line[4:7]
    data["county name"]         = unicode(line[7:71].strip(), "latin1")
    data["Total population"]    = int(line[71:80].strip())
    data["Total Housing Units"] = int(line[80:89].strip())
    data["Land area msq"]       = int(line[89:103].strip())
    data["Water area msq"]      = int(line[103:117].strip())
    latlng = [ float(line[141:151].strip()), float(line[151:162].strip()) ]
    scraperwiki.datastore.save(unique_keys=["FIPS state code", "FIPS county code"], data=data, latlng=latlng, silent=True)
    totallandareamsq += data["Land area msq"]
    totalwaterareamsq += data["Water area msq"]

print "Total land area=%.1f m^2, Total water area=%.1f m^2" % (totallandareamsq, totalwaterareamsq)

# (check why I need unicode(latin1) here as I thought I was trapping such exceptions 
# before they reached the JSON encoding stage)
import scraperwiki
import urllib

# Documentation for file standard:
#http://www.census.gov/geo/www/gazetteer/places2k_layout.html#counties

fin = urllib.urlopen("http://www.census.gov/tiger/tms/gazetteer/county2k.txt")

totallandareamsq = 0.0
totalwaterareamsq = 0.0

for line in fin.readlines():
    data = { }
    data["state"]               = line[0:2]
    data["FIPS state code"]     = line[2:4]
    data["FIPS county code"]    = line[4:7]
    data["county name"]         = unicode(line[7:71].strip(), "latin1")
    data["Total population"]    = int(line[71:80].strip())
    data["Total Housing Units"] = int(line[80:89].strip())
    data["Land area msq"]       = int(line[89:103].strip())
    data["Water area msq"]      = int(line[103:117].strip())
    latlng = [ float(line[141:151].strip()), float(line[151:162].strip()) ]
    scraperwiki.datastore.save(unique_keys=["FIPS state code", "FIPS county code"], data=data, latlng=latlng, silent=True)
    totallandareamsq += data["Land area msq"]
    totalwaterareamsq += data["Water area msq"]

print "Total land area=%.1f m^2, Total water area=%.1f m^2" % (totallandareamsq, totalwaterareamsq)

# (check why I need unicode(latin1) here as I thought I was trapping such exceptions 
# before they reached the JSON encoding stage)
import scraperwiki
import urllib

# Documentation for file standard:
#http://www.census.gov/geo/www/gazetteer/places2k_layout.html#counties

fin = urllib.urlopen("http://www.census.gov/tiger/tms/gazetteer/county2k.txt")

totallandareamsq = 0.0
totalwaterareamsq = 0.0

for line in fin.readlines():
    data = { }
    data["state"]               = line[0:2]
    data["FIPS state code"]     = line[2:4]
    data["FIPS county code"]    = line[4:7]
    data["county name"]         = unicode(line[7:71].strip(), "latin1")
    data["Total population"]    = int(line[71:80].strip())
    data["Total Housing Units"] = int(line[80:89].strip())
    data["Land area msq"]       = int(line[89:103].strip())
    data["Water area msq"]      = int(line[103:117].strip())
    latlng = [ float(line[141:151].strip()), float(line[151:162].strip()) ]
    scraperwiki.datastore.save(unique_keys=["FIPS state code", "FIPS county code"], data=data, latlng=latlng, silent=True)
    totallandareamsq += data["Land area msq"]
    totalwaterareamsq += data["Water area msq"]

print "Total land area=%.1f m^2, Total water area=%.1f m^2" % (totallandareamsq, totalwaterareamsq)

# (check why I need unicode(latin1) here as I thought I was trapping such exceptions 
# before they reached the JSON encoding stage)
