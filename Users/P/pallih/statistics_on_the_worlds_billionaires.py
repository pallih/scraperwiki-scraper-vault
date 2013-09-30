#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki
sourcescraper = "forbes_the_world_billionaires_2011"





# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata")
keys = sdata.get("keys")
rows = sdata.get("data")

# make a list of all the values for each key
valuelists = { }
for key in keys:
    valuelists[key] = [ ]   # list of empty lists for our values

for row in rows:
    for key, value in zip(keys, row):
        valuelists[key].append(value)
        #print value

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
    dups = [ (v, str(k))  for k, v in counts.items() ]
    print type(dups)
    dups.sort(reverse=True)
    medduppercent = dups[len(dups)/2][0]*100.0/len(valuelist)
    print "%d distinct values from a total of %d; median duplicates=%.0f%%<br/>" % (len(counts), len(valuelist), medduppercent)
    for i in range(min(10, len(dups))):
        key = dups[i][1]
        if not key:
            key = "None"
        if len(key) > 90:
            key = "%s...%s" % (key[:70], key[-20:])
        print "<em>%s</em> : %d (%.00f%%)<br/>" % (key, dups[i][0], float(dups[i][0])/len(valuelist)*100.00 )
        

    print "<br/>"
    

# Report on the types and ranges of values associated to each key
print '<h2>The world billionaires</h2>'
print '<h3>Statistics on data from the <a href="http://scraperwiki.com/scrapers/forbes_the_world_billionaires_2011/">Forbes list of world billionaires</a> scraper</h3>'
print "<dl>"
for key in keys:
    valuelist = valuelists[key]
    if key == 'name':
        pass
    elif key == 'rank':
        pass
    elif key == 'worth':
        pass
        
    else:
        print "<dt><b>%s</b></dt>" % key
        print "<dd>"

        DetectNumerics(valuelist)
        DetectDuplicates(valuelist)

    print "</dd>"

print "</dl>"


    #########################################
# Simple table of values from one scraper
#########################################
import scraperwiki
sourcescraper = "forbes_the_world_billionaires_2011"





# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.swdata")
keys = sdata.get("keys")
rows = sdata.get("data")

# make a list of all the values for each key
valuelists = { }
for key in keys:
    valuelists[key] = [ ]   # list of empty lists for our values

for row in rows:
    for key, value in zip(keys, row):
        valuelists[key].append(value)
        #print value

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
    dups = [ (v, str(k))  for k, v in counts.items() ]
    print type(dups)
    dups.sort(reverse=True)
    medduppercent = dups[len(dups)/2][0]*100.0/len(valuelist)
    print "%d distinct values from a total of %d; median duplicates=%.0f%%<br/>" % (len(counts), len(valuelist), medduppercent)
    for i in range(min(10, len(dups))):
        key = dups[i][1]
        if not key:
            key = "None"
        if len(key) > 90:
            key = "%s...%s" % (key[:70], key[-20:])
        print "<em>%s</em> : %d (%.00f%%)<br/>" % (key, dups[i][0], float(dups[i][0])/len(valuelist)*100.00 )
        

    print "<br/>"
    

# Report on the types and ranges of values associated to each key
print '<h2>The world billionaires</h2>'
print '<h3>Statistics on data from the <a href="http://scraperwiki.com/scrapers/forbes_the_world_billionaires_2011/">Forbes list of world billionaires</a> scraper</h3>'
print "<dl>"
for key in keys:
    valuelist = valuelists[key]
    if key == 'name':
        pass
    elif key == 'rank':
        pass
    elif key == 'worth':
        pass
        
    else:
        print "<dt><b>%s</b></dt>" % key
        print "<dd>"

        DetectNumerics(valuelist)
        DetectDuplicates(valuelist)

    print "</dd>"

print "</dl>"


    