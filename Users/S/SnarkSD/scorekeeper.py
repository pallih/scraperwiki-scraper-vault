import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "2011-2012s"
gidarray = [20001]
PPT = [0,0]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21230):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20112012/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    i = 0
    TeamHG = 0
    TeamHS = 0
    TeamHM = 0
    TeamHB = 0
    TeamHH = 0
    TeamHT = 0
    TeamHGI = 0
    TeamAG = 0
    TeamAS = 0
    TeamAM = 0
    TeamAB = 0
    TeamAH = 0
    TeamAT = 0
    TeamAGI = 0

    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]

    tds = root.cssselect("tr.evenColor td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="GOAL"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHG += 1
            else:
                TeamAG += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="SHOT"):
            if (tds[i + 1].text.startswith(hometeam)):
                TeamHS += 1
            else:
                TeamAS += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="MISS"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHM += 1
            else:
                TeamAM += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="BLOCK"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHB += 1
            else:
                TeamAB += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="HIT"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHH += 1
            else:
                TeamAH += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="GIVE"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHGI += 1
            else:
                TeamAGI += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="TAKE"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHT += 1
            else:
                TeamAT += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="FAC"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHT += 1
            else:
                TeamAT += 1
        i += 1
    time.sleep(3) # delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/20112012/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    i = 0
    m = 1
    PPT = [0,0]
    tds = root.cssselect("td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        print i, td, td.text, td.datetime
        #try:
            #if 'SCORING SUMMARY' in td.text:
                #for m 
        #except TypeError:
            #pass
        try:
            if 'Goals-Opp./PPTime' in td.text:
                PPT[m] = tds[i+2].text
                m -= 1
        except TypeError:
            pass
        i += 1
    save = [hometeam, awayteam, season, gid, TeamHG, TeamHS, TeamHM, TeamHB, TeamHH, TeamHT, TeamHGI, TeamAG, TeamAS, TeamAM, TeamAB, TeamAH, TeamAT, TeamAGI,PPT]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    time.sleep(3) # delay X seconds to throttle URL fetching
import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "2011-2012s"
gidarray = [20001]
PPT = [0,0]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21230):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20112012/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    i = 0
    TeamHG = 0
    TeamHS = 0
    TeamHM = 0
    TeamHB = 0
    TeamHH = 0
    TeamHT = 0
    TeamHGI = 0
    TeamAG = 0
    TeamAS = 0
    TeamAM = 0
    TeamAB = 0
    TeamAH = 0
    TeamAT = 0
    TeamAGI = 0

    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]

    tds = root.cssselect("tr.evenColor td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="GOAL"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHG += 1
            else:
                TeamAG += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="SHOT"):
            if (tds[i + 1].text.startswith(hometeam)):
                TeamHS += 1
            else:
                TeamAS += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="MISS"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHM += 1
            else:
                TeamAM += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="BLOCK"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHB += 1
            else:
                TeamAB += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="HIT"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHH += 1
            else:
                TeamAH += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="GIVE"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHGI += 1
            else:
                TeamAGI += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="TAKE"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHT += 1
            else:
                TeamAT += 1
        elif ((tds[i-3].text != "5" or tds[i-3].text != "4") and td.text =="FAC"):
            if tds[i + 1].text.startswith(hometeam):
                TeamHT += 1
            else:
                TeamAT += 1
        i += 1
    time.sleep(3) # delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/20112012/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    i = 0
    m = 1
    PPT = [0,0]
    tds = root.cssselect("td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        print i, td, td.text, td.datetime
        #try:
            #if 'SCORING SUMMARY' in td.text:
                #for m 
        #except TypeError:
            #pass
        try:
            if 'Goals-Opp./PPTime' in td.text:
                PPT[m] = tds[i+2].text
                m -= 1
        except TypeError:
            pass
        i += 1
    save = [hometeam, awayteam, season, gid, TeamHG, TeamHS, TeamHM, TeamHB, TeamHH, TeamHT, TeamHGI, TeamAG, TeamAS, TeamAM, TeamAB, TeamAH, TeamAT, TeamAGI,PPT]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    time.sleep(3) # delay X seconds to throttle URL fetching
