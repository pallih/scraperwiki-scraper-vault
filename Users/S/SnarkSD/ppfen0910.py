import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "2009-2010s"
gidarray = [20081, 21157]
PPT = [0,0]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),(scraperwiki.sqlite.get_var('gid') + 1230)):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20092010/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    i = 0
    TeamHG = 0
    TeamHS = 0
    TeamHM = 0
    TeamHF = 0
    TeamHB = 0
    TeamHC = 0
    TeamAG = 0
    TeamAS = 0
    TeamAM = 0
    TeamAF = 0
    TeamAB = 0
    TeamAC = 0

    STeamHG = 0
    STeamHS = 0
    STeamHM = 0
    STeamHF = 0
    STeamHB = 0
    STeamHC = 0
    STeamAG = 0
    STeamAS = 0
    STeamAM = 0
    STeamAF = 0
    STeamAB = 0
    STeamAC = 0

    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    
    tds = root.cssselect("tr.evenColor td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if ((tds[i-3].text != "5") and td.text =="GOAL") and (tds[i-2].text == "PP"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                TeamHG += 1
            elif ('G' in awayskate and 'G' in homeskate):
                TeamAG += 1
        elif ((tds[i-3].text != "5") and td.text =="SHOT")  and (tds[i-2].text == "PP"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                TeamHS += 1
            elif ('G' in awayskate and 'G' in homeskate):
                TeamAS += 1
        elif ((tds[i-3].text != "5") and td.text =="MISS")  and (tds[i-2].text == "PP"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                TeamHM += 1
            elif ('G' in awayskate and 'G' in homeskate):
                TeamAM += 1
        elif ((tds[i-3].text != "5") and td.text =="BLOCK")  and (tds[i-2].text == "SH"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                TeamHB += 1
            elif ('G' in awayskate and 'G' in homeskate):
                TeamAB += 1
        if ((tds[i-3].text != "5") and td.text =="GOAL") and (tds[i-2].text == "SH"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                STeamHG += 1
            elif ('G' in awayskate and 'G' in homeskate):
                STeamAG += 1
        elif ((tds[i-3].text != "5") and td.text =="SHOT")  and (tds[i-2].text == "SH"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                STeamHS += 1
            elif ('G' in awayskate and 'G' in homeskate):
                STeamAS += 1
        elif ((tds[i-3].text != "5") and td.text =="MISS")  and (tds[i-2].text == "SH"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                STeamHM += 1
            elif ('G' in awayskate and 'G' in homeskate):
                STeamAM += 1
        elif ((tds[i-3].text != "5") and td.text =="BLOCK")  and (tds[i-2].text == "PP"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                STeamHB += 1
            elif ('G' in awayskate and 'G' in homeskate):
                STeamAB += 1
        i += 1
    TeamHF = TeamHG + TeamHS + TeamHM
    TeamAF = TeamAG + TeamAS + TeamAM
    TeamHC = TeamHF + TeamHB
    TeamAC = TeamAF + TeamAB
    STeamHF = STeamHG + STeamHS + STeamHM
    STeamAF = STeamAG + STeamAS + STeamAM
    STeamHC = STeamHF + STeamHB
    STeamAC = STeamAF + STeamAB
    time.sleep(3) # delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/20092010/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    i = 0
    PPT = [0,0]
    tds = root.cssselect("td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        print i, td.text
        try:
            if "Power Play Time" in td.text:
                PPT[1] = tds[i+10].text
                PPT[0] = tds[i+19].text
        except TypeError:
            pass
        i += 1
    save = [hometeam, awayteam, season, gid, TeamHG, TeamHS, TeamHF, TeamHC, TeamAG, TeamAS, TeamAF, TeamAC, STeamHG, STeamHS, STeamHF, STeamHC, STeamAG, STeamAS, STeamAF, STeamAC, PPT]
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
season = "2009-2010s"
gidarray = [20081, 21157]
PPT = [0,0]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),(scraperwiki.sqlite.get_var('gid') + 1230)):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20092010/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    i = 0
    TeamHG = 0
    TeamHS = 0
    TeamHM = 0
    TeamHF = 0
    TeamHB = 0
    TeamHC = 0
    TeamAG = 0
    TeamAS = 0
    TeamAM = 0
    TeamAF = 0
    TeamAB = 0
    TeamAC = 0

    STeamHG = 0
    STeamHS = 0
    STeamHM = 0
    STeamHF = 0
    STeamHB = 0
    STeamHC = 0
    STeamAG = 0
    STeamAS = 0
    STeamAM = 0
    STeamAF = 0
    STeamAB = 0
    STeamAC = 0

    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    
    tds = root.cssselect("tr.evenColor td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if ((tds[i-3].text != "5") and td.text =="GOAL") and (tds[i-2].text == "PP"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                TeamHG += 1
            elif ('G' in awayskate and 'G' in homeskate):
                TeamAG += 1
        elif ((tds[i-3].text != "5") and td.text =="SHOT")  and (tds[i-2].text == "PP"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                TeamHS += 1
            elif ('G' in awayskate and 'G' in homeskate):
                TeamAS += 1
        elif ((tds[i-3].text != "5") and td.text =="MISS")  and (tds[i-2].text == "PP"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                TeamHM += 1
            elif ('G' in awayskate and 'G' in homeskate):
                TeamAM += 1
        elif ((tds[i-3].text != "5") and td.text =="BLOCK")  and (tds[i-2].text == "SH"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                TeamHB += 1
            elif ('G' in awayskate and 'G' in homeskate):
                TeamAB += 1
        if ((tds[i-3].text != "5") and td.text =="GOAL") and (tds[i-2].text == "SH"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                STeamHG += 1
            elif ('G' in awayskate and 'G' in homeskate):
                STeamAG += 1
        elif ((tds[i-3].text != "5") and td.text =="SHOT")  and (tds[i-2].text == "SH"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                STeamHS += 1
            elif ('G' in awayskate and 'G' in homeskate):
                STeamAS += 1
        elif ((tds[i-3].text != "5") and td.text =="MISS")  and (tds[i-2].text == "SH"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                STeamHM += 1
            elif ('G' in awayskate and 'G' in homeskate):
                STeamAM += 1
        elif ((tds[i-3].text != "5") and td.text =="BLOCK")  and (tds[i-2].text == "PP"):
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and tds[i + 1].text.startswith(hometeam):
                STeamHB += 1
            elif ('G' in awayskate and 'G' in homeskate):
                STeamAB += 1
        i += 1
    TeamHF = TeamHG + TeamHS + TeamHM
    TeamAF = TeamAG + TeamAS + TeamAM
    TeamHC = TeamHF + TeamHB
    TeamAC = TeamAF + TeamAB
    STeamHF = STeamHG + STeamHS + STeamHM
    STeamAF = STeamAG + STeamAS + STeamAM
    STeamHC = STeamHF + STeamHB
    STeamAC = STeamAF + STeamAB
    time.sleep(3) # delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/20092010/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    i = 0
    PPT = [0,0]
    tds = root.cssselect("td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        print i, td.text
        try:
            if "Power Play Time" in td.text:
                PPT[1] = tds[i+10].text
                PPT[0] = tds[i+19].text
        except TypeError:
            pass
        i += 1
    save = [hometeam, awayteam, season, gid, TeamHG, TeamHS, TeamHF, TeamHC, TeamAG, TeamAS, TeamAF, TeamAC, STeamHG, STeamHS, STeamHF, STeamHC, STeamAG, STeamAS, STeamAF, STeamAC, PPT]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    time.sleep(3) # delay X seconds to throttle URL fetching
