#########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "information-asset-register"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

# make a list of all the values for each key
keys = getKeys(sourcescraper)
keys.sort()
valuelists = dict(zip(keys, [ []  for i in range(len(keys))]))   # list of empty lists for our values

for row in getData(sourcescraper, limit, offset):
    for key in keys:
        valuelists[key].append(row.get(key))


# detect and analyze the numeric component of this value
def DetectNumerics(valuelist):
    int_n = 0
    float_n = 0
    float_min = 0.0
    float_max = 0.0
    float_sum = 0.0

    for value in valuelist:
        try:
            fvalue = float(value)
            if float_n == 0 or fvalue < float_min:
                float_min = fvalue
            if float_n == 0 or fvalue > float_max:
                float_max = fvalue
            float_sum += fvalue
            float_n += 1
            
            ivalue = int(value)  # this will throw an exception if there is a decimal
            int_n += 1
        except ValueError, e:
            pass
        except TypeError, e:
            pass
        
    if float_n != 0:
        print " %.0f%% are numeric (%.0f%% are integral)" % (float_n*100.0/len(valuelist), int_n*100.0/len(valuelist)),
        print " min=%f max=%f avg=%f<br/>" % (float_min, float_max, float_sum/len(valuelist))
    
        
def DetectDuplicates(valuelist):
    counts = { }
    for value in valuelist:
        counts[value] = counts.setdefault(value, 0) + 1
    dups = [ (v, k)  for k, v in counts.items() ]
    dups.sort(reverse=True)
    medduppercent = dups[len(dups)/2][0]*100.0/len(valuelist)
    print "%d distinct values from a total of %d; median duplicates=%.0f%%<br/>" % (len(counts), len(valuelist), medduppercent)
    for i in range(min(5, len(dups))):
        key = dups[i][1]
        if not key:
            key = "None"
        if len(key) > 90:
            key = "%s...%s" % (key[:70], key[-20:])
        print "<em>%s</em> : %d<br/>" % (key, dups[i][0]),
    print "<br/>"
    
    
def DetectLatlngRange(valuelist):
    latlng_n = 0
    lat_min = 0.0
    lat_max = 0.0
    lng_min = 0.0
    lng_max = 0.0
    for value in valuelist:
        if value:
            lat, lng = value
            if latlng_n == 0 or lat < lat_min:
                lat_min = lat
            if latlng_n == 0 or lat > lat_max:
                lat_max = lat
            if latlng_n == 0 or lng < lng_min:
                lng_min = lng
            if latlng_n == 0 or lng > lng_max:
                lng_max = lng
            latlng_n += 1

    if latlng_n != 0:
        print " %.0f%% have grid coordinates range lat=[%.3f, %.3f], lng=[%.3f, %.3f]<br/>" % \
                (latlng_n*100/len(valuelist), lat_min, lat_max, lng_min, lng_max)
    

# Report on the types and ranges of values associated to each key
print '<h2>Analyse the range and data for each key in scraper: %s</h2>' % sourcescraper
print "<dl>"
for key in keys:
    print "<dt><b>%s</b></dt>" % key
    valuelist = valuelists[key]
    print "<dd>"
    if key == 'latlng':
        DetectLatlngRange(valuelist)
      # need to add a date range detecting one here too
    else:
        DetectNumerics(valuelist)
        DetectDuplicates(valuelist)

    print "</dd>"

print "</dl>"

    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "information-asset-register"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

# make a list of all the values for each key
keys = getKeys(sourcescraper)
keys.sort()
valuelists = dict(zip(keys, [ []  for i in range(len(keys))]))   # list of empty lists for our values

for row in getData(sourcescraper, limit, offset):
    for key in keys:
        valuelists[key].append(row.get(key))


# detect and analyze the numeric component of this value
def DetectNumerics(valuelist):
    int_n = 0
    float_n = 0
    float_min = 0.0
    float_max = 0.0
    float_sum = 0.0

    for value in valuelist:
        try:
            fvalue = float(value)
            if float_n == 0 or fvalue < float_min:
                float_min = fvalue
            if float_n == 0 or fvalue > float_max:
                float_max = fvalue
            float_sum += fvalue
            float_n += 1
            
            ivalue = int(value)  # this will throw an exception if there is a decimal
            int_n += 1
        except ValueError, e:
            pass
        except TypeError, e:
            pass
        
    if float_n != 0:
        print " %.0f%% are numeric (%.0f%% are integral)" % (float_n*100.0/len(valuelist), int_n*100.0/len(valuelist)),
        print " min=%f max=%f avg=%f<br/>" % (float_min, float_max, float_sum/len(valuelist))
    
        
def DetectDuplicates(valuelist):
    counts = { }
    for value in valuelist:
        counts[value] = counts.setdefault(value, 0) + 1
    dups = [ (v, k)  for k, v in counts.items() ]
    dups.sort(reverse=True)
    medduppercent = dups[len(dups)/2][0]*100.0/len(valuelist)
    print "%d distinct values from a total of %d; median duplicates=%.0f%%<br/>" % (len(counts), len(valuelist), medduppercent)
    for i in range(min(5, len(dups))):
        key = dups[i][1]
        if not key:
            key = "None"
        if len(key) > 90:
            key = "%s...%s" % (key[:70], key[-20:])
        print "<em>%s</em> : %d<br/>" % (key, dups[i][0]),
    print "<br/>"
    
    
def DetectLatlngRange(valuelist):
    latlng_n = 0
    lat_min = 0.0
    lat_max = 0.0
    lng_min = 0.0
    lng_max = 0.0
    for value in valuelist:
        if value:
            lat, lng = value
            if latlng_n == 0 or lat < lat_min:
                lat_min = lat
            if latlng_n == 0 or lat > lat_max:
                lat_max = lat
            if latlng_n == 0 or lng < lng_min:
                lng_min = lng
            if latlng_n == 0 or lng > lng_max:
                lng_max = lng
            latlng_n += 1

    if latlng_n != 0:
        print " %.0f%% have grid coordinates range lat=[%.3f, %.3f], lng=[%.3f, %.3f]<br/>" % \
                (latlng_n*100/len(valuelist), lat_min, lat_max, lng_min, lng_max)
    

# Report on the types and ranges of values associated to each key
print '<h2>Analyse the range and data for each key in scraper: %s</h2>' % sourcescraper
print "<dl>"
for key in keys:
    print "<dt><b>%s</b></dt>" % key
    valuelist = valuelists[key]
    print "<dd>"
    if key == 'latlng':
        DetectLatlngRange(valuelist)
      # need to add a date range detecting one here too
    else:
        DetectNumerics(valuelist)
        DetectDuplicates(valuelist)

    print "</dd>"

print "</dl>"

    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "information-asset-register"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

# make a list of all the values for each key
keys = getKeys(sourcescraper)
keys.sort()
valuelists = dict(zip(keys, [ []  for i in range(len(keys))]))   # list of empty lists for our values

for row in getData(sourcescraper, limit, offset):
    for key in keys:
        valuelists[key].append(row.get(key))


# detect and analyze the numeric component of this value
def DetectNumerics(valuelist):
    int_n = 0
    float_n = 0
    float_min = 0.0
    float_max = 0.0
    float_sum = 0.0

    for value in valuelist:
        try:
            fvalue = float(value)
            if float_n == 0 or fvalue < float_min:
                float_min = fvalue
            if float_n == 0 or fvalue > float_max:
                float_max = fvalue
            float_sum += fvalue
            float_n += 1
            
            ivalue = int(value)  # this will throw an exception if there is a decimal
            int_n += 1
        except ValueError, e:
            pass
        except TypeError, e:
            pass
        
    if float_n != 0:
        print " %.0f%% are numeric (%.0f%% are integral)" % (float_n*100.0/len(valuelist), int_n*100.0/len(valuelist)),
        print " min=%f max=%f avg=%f<br/>" % (float_min, float_max, float_sum/len(valuelist))
    
        
def DetectDuplicates(valuelist):
    counts = { }
    for value in valuelist:
        counts[value] = counts.setdefault(value, 0) + 1
    dups = [ (v, k)  for k, v in counts.items() ]
    dups.sort(reverse=True)
    medduppercent = dups[len(dups)/2][0]*100.0/len(valuelist)
    print "%d distinct values from a total of %d; median duplicates=%.0f%%<br/>" % (len(counts), len(valuelist), medduppercent)
    for i in range(min(5, len(dups))):
        key = dups[i][1]
        if not key:
            key = "None"
        if len(key) > 90:
            key = "%s...%s" % (key[:70], key[-20:])
        print "<em>%s</em> : %d<br/>" % (key, dups[i][0]),
    print "<br/>"
    
    
def DetectLatlngRange(valuelist):
    latlng_n = 0
    lat_min = 0.0
    lat_max = 0.0
    lng_min = 0.0
    lng_max = 0.0
    for value in valuelist:
        if value:
            lat, lng = value
            if latlng_n == 0 or lat < lat_min:
                lat_min = lat
            if latlng_n == 0 or lat > lat_max:
                lat_max = lat
            if latlng_n == 0 or lng < lng_min:
                lng_min = lng
            if latlng_n == 0 or lng > lng_max:
                lng_max = lng
            latlng_n += 1

    if latlng_n != 0:
        print " %.0f%% have grid coordinates range lat=[%.3f, %.3f], lng=[%.3f, %.3f]<br/>" % \
                (latlng_n*100/len(valuelist), lat_min, lat_max, lng_min, lng_max)
    

# Report on the types and ranges of values associated to each key
print '<h2>Analyse the range and data for each key in scraper: %s</h2>' % sourcescraper
print "<dl>"
for key in keys:
    print "<dt><b>%s</b></dt>" % key
    valuelist = valuelists[key]
    print "<dd>"
    if key == 'latlng':
        DetectLatlngRange(valuelist)
      # need to add a date range detecting one here too
    else:
        DetectNumerics(valuelist)
        DetectDuplicates(valuelist)

    print "</dd>"

print "</dl>"

    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "information-asset-register"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

# make a list of all the values for each key
keys = getKeys(sourcescraper)
keys.sort()
valuelists = dict(zip(keys, [ []  for i in range(len(keys))]))   # list of empty lists for our values

for row in getData(sourcescraper, limit, offset):
    for key in keys:
        valuelists[key].append(row.get(key))


# detect and analyze the numeric component of this value
def DetectNumerics(valuelist):
    int_n = 0
    float_n = 0
    float_min = 0.0
    float_max = 0.0
    float_sum = 0.0

    for value in valuelist:
        try:
            fvalue = float(value)
            if float_n == 0 or fvalue < float_min:
                float_min = fvalue
            if float_n == 0 or fvalue > float_max:
                float_max = fvalue
            float_sum += fvalue
            float_n += 1
            
            ivalue = int(value)  # this will throw an exception if there is a decimal
            int_n += 1
        except ValueError, e:
            pass
        except TypeError, e:
            pass
        
    if float_n != 0:
        print " %.0f%% are numeric (%.0f%% are integral)" % (float_n*100.0/len(valuelist), int_n*100.0/len(valuelist)),
        print " min=%f max=%f avg=%f<br/>" % (float_min, float_max, float_sum/len(valuelist))
    
        
def DetectDuplicates(valuelist):
    counts = { }
    for value in valuelist:
        counts[value] = counts.setdefault(value, 0) + 1
    dups = [ (v, k)  for k, v in counts.items() ]
    dups.sort(reverse=True)
    medduppercent = dups[len(dups)/2][0]*100.0/len(valuelist)
    print "%d distinct values from a total of %d; median duplicates=%.0f%%<br/>" % (len(counts), len(valuelist), medduppercent)
    for i in range(min(5, len(dups))):
        key = dups[i][1]
        if not key:
            key = "None"
        if len(key) > 90:
            key = "%s...%s" % (key[:70], key[-20:])
        print "<em>%s</em> : %d<br/>" % (key, dups[i][0]),
    print "<br/>"
    
    
def DetectLatlngRange(valuelist):
    latlng_n = 0
    lat_min = 0.0
    lat_max = 0.0
    lng_min = 0.0
    lng_max = 0.0
    for value in valuelist:
        if value:
            lat, lng = value
            if latlng_n == 0 or lat < lat_min:
                lat_min = lat
            if latlng_n == 0 or lat > lat_max:
                lat_max = lat
            if latlng_n == 0 or lng < lng_min:
                lng_min = lng
            if latlng_n == 0 or lng > lng_max:
                lng_max = lng
            latlng_n += 1

    if latlng_n != 0:
        print " %.0f%% have grid coordinates range lat=[%.3f, %.3f], lng=[%.3f, %.3f]<br/>" % \
                (latlng_n*100/len(valuelist), lat_min, lat_max, lng_min, lng_max)
    

# Report on the types and ranges of values associated to each key
print '<h2>Analyse the range and data for each key in scraper: %s</h2>' % sourcescraper
print "<dl>"
for key in keys:
    print "<dt><b>%s</b></dt>" % key
    valuelist = valuelists[key]
    print "<dd>"
    if key == 'latlng':
        DetectLatlngRange(valuelist)
      # need to add a date range detecting one here too
    else:
        DetectNumerics(valuelist)
        DetectDuplicates(valuelist)

    print "</dd>"

print "</dl>"

    #########################################
# Simple table of values from one scraper
#########################################
from scraperwiki.apiwrapper import getKeys, getData, getDataByDate, getDataByLocation

sourcescraper = "information-asset-register"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 200  
offset = 0

# make a list of all the values for each key
keys = getKeys(sourcescraper)
keys.sort()
valuelists = dict(zip(keys, [ []  for i in range(len(keys))]))   # list of empty lists for our values

for row in getData(sourcescraper, limit, offset):
    for key in keys:
        valuelists[key].append(row.get(key))


# detect and analyze the numeric component of this value
def DetectNumerics(valuelist):
    int_n = 0
    float_n = 0
    float_min = 0.0
    float_max = 0.0
    float_sum = 0.0

    for value in valuelist:
        try:
            fvalue = float(value)
            if float_n == 0 or fvalue < float_min:
                float_min = fvalue
            if float_n == 0 or fvalue > float_max:
                float_max = fvalue
            float_sum += fvalue
            float_n += 1
            
            ivalue = int(value)  # this will throw an exception if there is a decimal
            int_n += 1
        except ValueError, e:
            pass
        except TypeError, e:
            pass
        
    if float_n != 0:
        print " %.0f%% are numeric (%.0f%% are integral)" % (float_n*100.0/len(valuelist), int_n*100.0/len(valuelist)),
        print " min=%f max=%f avg=%f<br/>" % (float_min, float_max, float_sum/len(valuelist))
    
        
def DetectDuplicates(valuelist):
    counts = { }
    for value in valuelist:
        counts[value] = counts.setdefault(value, 0) + 1
    dups = [ (v, k)  for k, v in counts.items() ]
    dups.sort(reverse=True)
    medduppercent = dups[len(dups)/2][0]*100.0/len(valuelist)
    print "%d distinct values from a total of %d; median duplicates=%.0f%%<br/>" % (len(counts), len(valuelist), medduppercent)
    for i in range(min(5, len(dups))):
        key = dups[i][1]
        if not key:
            key = "None"
        if len(key) > 90:
            key = "%s...%s" % (key[:70], key[-20:])
        print "<em>%s</em> : %d<br/>" % (key, dups[i][0]),
    print "<br/>"
    
    
def DetectLatlngRange(valuelist):
    latlng_n = 0
    lat_min = 0.0
    lat_max = 0.0
    lng_min = 0.0
    lng_max = 0.0
    for value in valuelist:
        if value:
            lat, lng = value
            if latlng_n == 0 or lat < lat_min:
                lat_min = lat
            if latlng_n == 0 or lat > lat_max:
                lat_max = lat
            if latlng_n == 0 or lng < lng_min:
                lng_min = lng
            if latlng_n == 0 or lng > lng_max:
                lng_max = lng
            latlng_n += 1

    if latlng_n != 0:
        print " %.0f%% have grid coordinates range lat=[%.3f, %.3f], lng=[%.3f, %.3f]<br/>" % \
                (latlng_n*100/len(valuelist), lat_min, lat_max, lng_min, lng_max)
    

# Report on the types and ranges of values associated to each key
print '<h2>Analyse the range and data for each key in scraper: %s</h2>' % sourcescraper
print "<dl>"
for key in keys:
    print "<dt><b>%s</b></dt>" % key
    valuelist = valuelists[key]
    print "<dd>"
    if key == 'latlng':
        DetectLatlngRange(valuelist)
      # need to add a date range detecting one here too
    else:
        DetectNumerics(valuelist)
        DetectDuplicates(valuelist)

    print "</dd>"

print "</dl>"

    