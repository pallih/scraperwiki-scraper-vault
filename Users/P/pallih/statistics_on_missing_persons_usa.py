#########################################
# Simple table of values from one scraper
#########################################
import scraperwiki
sourcescraper = "missing_persons_usa"

# a bigger limit will get a more representative sample.  
# or set a high offset to get a different sample
limit = 6000  
offset = 0

# connect to the source database giving it the name src
scraperwiki.sqlite.attach(sourcescraper, "src")

# the default table in most scrapers is called swdata
sdata = scraperwiki.sqlite.execute("select * from src.missing_persons_usa limit ? offset ?", (limit, offset))
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
print '<h2>Missing persons USA</h2>'
print '<h3>Statistics on data from the <a href="http://scraperwiki.com/scrapers/missing_persons_usa/">Missing persons USA</a> scraper</h3>'
print "<dl>"
for key in keys:
    print "<dt><b>%s</b></dt>" % key
    valuelist = valuelists[key]
    print "<dd>"
    if key == 'id':
        pass
    elif key == 'detail_url':
        pass
    elif key == 'date':
        pass
    elif key == 'name':
        pass
    elif key == 'location':
        pass
    # need to add a date range detecting one here too
    else:
        DetectNumerics(valuelist)
        DetectDuplicates(valuelist)

    print "</dd>"

print "</dl>"

    