import dateutil.parser
import urllib
import urllib2
import lxml
import lxml.html

import scraperwiki

print "Start" 

parkrun_url = "http://www.parkrun.org.uk/%s/results/latestresults"

runs = []
runnames = []

def get_runs():
    req = urllib2.Request("http://www.parkrun.org.uk/results/firstfinishers/")
    
    req.add_header("User-Agent", "Mozilla")
    req.add_header("Host", "www.parkrun.org.uk")
    req.add_header("Accept", "*/*")
    
    r = urllib2.urlopen(req)
    text = r.read()
    
    html = lxml.html.document_fromstring(text)
    # Hurts my eyes to do this, fragile as hell way
    # to get the race ID and date
    d = html.get_element_by_id("content")
    runs_rows = list(d.cssselect("table.sortable"))[0][1]
        
    for row in runs_rows:
        name = row.cssselect("td")[0].text_content()        
        el = row.cssselect("td a")[0]
        linkparts = el.get('href').split('/')
        racelink = linkparts[len(linkparts) - 2]                          
        runs.append(racelink)
        runnames.append(name)
        #print name

parkrun_url = "http://www.parkrun.org.uk/%s/results/latestresults"
parkrun_url2 = "http://www.parkrun.org.uk/%s/results/latestresults/"

keys = ["racedate", "name", "position", "time"]  

def get_results(index):  
    print "Getting retuls for " + runnames[index]    
    req = urllib2.Request(parkrun_url%(runs[index]))
    req.add_header("User-Agent", "Mozilla")
    req.add_header("Host", "www.parkrun.org.uk")
    req.add_header("Accept", "*/*")
    r = urllib2.urlopen(req)
    code = r.getcode()    
    #print code

    text = r.read()
    html = lxml.html.document_fromstring(text)

    # Hurts my eyes to do this, fragile as hell way
    # to get the race ID and date
    ab = 0
    try:
        d = html.get_element_by_id("dnn_ContentPane")
        ab = len(d.text_content())
    except:
        pass
    
    #print ab
    if ab == 0:
        #print "New Style"
        d = html.get_element_by_id("content")

    racename = d.cssselect("h2")[0].text_content()
    racerealname = racename.split('#')[0].strip()
    raceid = racename.split('\n')[1].strip().replace("-","").strip()
    racedate = dateutil.parser.parse(racename.split('\n')[2].strip(),
                                     dayfirst=True)
    #assert(int(raceid) == race)
    #print racename
    
    results_rows = list(html.get_element_by_id("results"))[1]
    
    racers = []
    
    #print results_rows
    for row in results_rows:
                
        vals = [td.text_content() for td in row]
        racer = dict()
              
        # Some racers have no times, skip them
        if not vals[2]:
            continue

        racer['position'] = int(vals[0])
        racer['name'] = vals[1]
        #min,sec = [int(d) for d in vals[2].split(":")]
        #racer['time'] = min + ":" + sec
        racer['time'] = vals[2]
        racer['agegroup'] = vals[3]
        racer['agegrade'] = vals[4]
        racer['gender'] = vals[5]
        racer['genderpos'] = int(vals[6])
        racer['club'] = vals[7]
        racer['note'] = vals[8]
        racer['totalruns'] = vals[9]
        racer['racename'] = racename
        racer['racedate'] = racedate
        #print racer    

        if "Beckenham RC" in racer['club']:    
            #http://www.parkrun.org.uk/athleteresultshistory?athleteNumber=46999
            el = row.cssselect("td a")[0]
            # get href attribute and strip athlete number        
            #print el         
            athnumber = el.get('href').split('=')[1].strip()
            racer['id'] = athnumber           
            #print athnumber            
            racers.append(racer)
    
    print "Finished getting results for " + racename    
    #print racers    
    #print racedate, len(racers)
    scraperwiki.sqlite.save(keys, racers, table_name="races")
    #scraperwiki.sqlite.save(keys, racers)

# Limit to first 50 races, could easily extend it to more
# and keep it up to date but for that we should find out
# scraping policy of parkrun.org

#runnames = ["bromley", "crystalpalace", "brockwell", "lloyd", "bexley", "dulwich", "greenwich", "hillyfields"]
#runs = ["bromley", "crystalpalace", "brockwell", "lloyd", "bexley", "dulwich", "greenwich","hillyfields"]
scraperwiki.sqlite.execute("delete from races")

doruns = get_runs()
#for race in range(20, 25):
for race in range(0, len(runs)):
    #print runnames[race]    
    try:
        res = get_results(race)
    except:
        pass




