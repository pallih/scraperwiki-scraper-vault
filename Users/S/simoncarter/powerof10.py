import dateutil.parser
import urllib
import urllib2
import lxml
import lxml.html

import scraperwiki

print "Start" 

poweroften_url = "http://www.thepowerof10.info/athletes/athleteslookup.aspx?surname=&firstname=&club=beckenham"

athletes = []

def get_athletes():
    req = urllib2.Request("http://www.thepowerof10.info/athletes/athleteslookup.aspx?surname=&firstname=&club=beckenham")
    
    req.add_header("User-Agent", "Mozilla")
    req.add_header("Host", "www.thepowerof10.info")
    req.add_header("Accept", "*/*")
    
    r = urllib2.urlopen(req)
    text = r.read()
    
    html = lxml.html.document_fromstring(text)
    # Hurts my eyes to do this, fragile as hell way
    # to get the race ID and date
    d = html.get_element_by_id("ctl00_cphBody_pnlResults")
    athlete_rows = list(d.cssselect("table#ctl00_cphBody_dgAthletes"))[0]
    
    for athlete in athlete_rows:
        firstname = athlete.cssselect("td")[0].text_content()
        secondname = athlete.cssselect("td")[1].text_content() 
        #print athlete
        el = athlete.cssselect("td")[7][0]
        #print firstname        
        #print el
        #linkparts = el.get('href').split('/')
        #racelink = linkparts[len(linkparts) - 2]                          
        racelink = el.get("href")
        print racelink        
        if not "First" in firstname:
            athletes.append(racelink)
        #print name

atheleteinfo_url = "http://www.thepowerof10.info/athletes/"

keys = ["racedate", "name", "position", "time"]  

def get_results(athleteurl):  
    print "Getting athlete info for ".join(athleteurl)
    req = urllib2.Request(atheleteinfo_url.athleteurl)
    
    req.add_header("User-Agent", "Mozilla")
    req.add_header("Host", "www.thepowerof10.info")
    req.add_header("Accept", "*/*")
    
    r = urllib2.urlopen(req)
    text = r.read()
    
    html = lxml.html.document_fromstring(text)
    # Hurts my eyes to do this, fragile as hell way
    # to get the race ID and date
    d = html.get_element_by_id("ctl00_cphBody_pnlMain")  
    athletename = d.cssselect("h2")[0].text_content()
    #racerealname = racename.split('#')[0].strip()
    #raceid = racename.split('\n')[1].strip().replace("-","").strip()
    #assert(int(raceid) == race)
    #print racename
    
    #results_rows = list(html.get_element_by_id("results"))[1]
    
    """
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
    
        if "Beckenham RC" in racer['club']:    
            #http://www.parkrun.org.uk/athleteresultshistory?athleteNumber=46999
            el = row.cssselect("td a")[0]
            # get href attribute and strip athlete number        
            #print el         
            athnumber = el.get('href').split('=')[1].strip()
            racer['id'] = athnumber           
            #print athnumber            
            racers.append(racer)
    
    #print racename    
    #print racers    
    #print racedate, len(racers)
    #scraperwiki.sqlite.save(keys, racers, table_name="athletes")
    #scraperwiki.sqlite.save(keys, racers)
"""

# Limit to first 50 races, could easily extend it to more
# and keep it up to date but for that we should find out
# scraping policy of parkrun.org

#runs = ["bromley", "crystalpalace", "brockwell", "lloyd", "bexley", "dulwich", "greenwich"]
#scraperwiki.sqlite.execute("delete from races")


doathletes = get_athletes()

for i in range(0, 2):
    res = get_results(athletes[i])    




