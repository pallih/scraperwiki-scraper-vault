import scraperwiki
import lxml.etree
import lxml.html
import datetime

#generate team id lists
teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]
teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]

#assign season in yearyear format, list of game IDs (gid) if necessary for scraping specific games
season = 20122013
gidarray = [20600]

#Scrape the Game summary page for basic data
#for gid in gidarray: #Specifies a specific range of game IDs to scrape. Uncomment, and comment out the next "for gid in range" statement 
if bool(scraperwiki.sqlite.get_var('gid')) == False: #Starts game ID at 20001 if no game id previously, ie. gid is empty
    scraperwiki.sqlite.save_var('gid', 20000)
for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21231): #
    seasongid = season*100000000 + gid*1000
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    date = root.cssselect("#GameInfo td")[3].text
    awayscore = root.cssselect("#Visitor td")[3].text
    homescore = root.cssselect("#Home td")[3].text

#Determine if the game went to OT or SO, and assign pointsbn
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    SOOT = 0
    for row in rows:
        table_cells = row.cssselect("td")
        if table_cells:
            if "OT" in table_cells[1].text:
                SOOT = 1
            elif "SO" in table_cells[1].text:
                SOOT = 2
    if homescore > awayscore and SOOT == 0:
        homepoints = 2
        awaypoints = 0
    elif homescore > awayscore and SOOT == 1 or SOOT == 2:
        homepoints = 2
        awaypoints = 1
    elif homescore < awayscore and SOOT == 0:
        homepoints = 0
        awaypoints = 2
    elif homescore < awayscore and SOOT == 1 or SOOT == 2:
        homepoints = 1
        awaypoints = 2

#PBP scrapper by rows of PBP data with 
    goaldiff = 0
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows = root.cssselect("tr.evenColor")
    for row in rows:
        tds = row.cssselect("td")
        seasongidevent = seasongid + int(tds[0].text)
        rowlist = [season, gid, seasongid, date, hometeam, homescore, awayteam, awayscore, SOOT, homepoints, awaypoints, goaldiff]
        if tds[4].text == 'GOAL' and tds[5].text.startswith(hometeam):
            goaldiff += 1
        elif tds[4].text == 'GOAL' and tds[5].text.startswith(awayteam):
            goaldiff -= 1
        for td in tds:
            rowlist.append(td.text)
        print scraperwiki.sqlite.save(unique_keys=['id'], data = {'id':seasongidevent, 'PBP_by_event':rowlist}, table_name="PBP")
import scraperwiki
import lxml.etree
import lxml.html
import datetime

#generate team id lists
teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]
teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]

#assign season in yearyear format, list of game IDs (gid) if necessary for scraping specific games
season = 20122013
gidarray = [20600]

#Scrape the Game summary page for basic data
#for gid in gidarray: #Specifies a specific range of game IDs to scrape. Uncomment, and comment out the next "for gid in range" statement 
if bool(scraperwiki.sqlite.get_var('gid')) == False: #Starts game ID at 20001 if no game id previously, ie. gid is empty
    scraperwiki.sqlite.save_var('gid', 20000)
for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21231): #
    seasongid = season*100000000 + gid*1000
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    date = root.cssselect("#GameInfo td")[3].text
    awayscore = root.cssselect("#Visitor td")[3].text
    homescore = root.cssselect("#Home td")[3].text

#Determine if the game went to OT or SO, and assign pointsbn
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    SOOT = 0
    for row in rows:
        table_cells = row.cssselect("td")
        if table_cells:
            if "OT" in table_cells[1].text:
                SOOT = 1
            elif "SO" in table_cells[1].text:
                SOOT = 2
    if homescore > awayscore and SOOT == 0:
        homepoints = 2
        awaypoints = 0
    elif homescore > awayscore and SOOT == 1 or SOOT == 2:
        homepoints = 2
        awaypoints = 1
    elif homescore < awayscore and SOOT == 0:
        homepoints = 0
        awaypoints = 2
    elif homescore < awayscore and SOOT == 1 or SOOT == 2:
        homepoints = 1
        awaypoints = 2

#PBP scrapper by rows of PBP data with 
    goaldiff = 0
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows = root.cssselect("tr.evenColor")
    for row in rows:
        tds = row.cssselect("td")
        seasongidevent = seasongid + int(tds[0].text)
        rowlist = [season, gid, seasongid, date, hometeam, homescore, awayteam, awayscore, SOOT, homepoints, awaypoints, goaldiff]
        if tds[4].text == 'GOAL' and tds[5].text.startswith(hometeam):
            goaldiff += 1
        elif tds[4].text == 'GOAL' and tds[5].text.startswith(awayteam):
            goaldiff -= 1
        for td in tds:
            rowlist.append(td.text)
        print scraperwiki.sqlite.save(unique_keys=['id'], data = {'id':seasongidevent, 'PBP_by_event':rowlist}, table_name="PBP")
