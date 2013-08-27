import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = 20122013
gidarray = [20074,    20427,    20668]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),20721):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    date = root.cssselect("#GameInfo td")[3].text
    awayscore = root.cssselect("#Visitor td")[3].text
    homescore = root.cssselect("#Home td")[3].text

# scrape_table function: gets passed an individual page to scrape
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
# Get PPTime
    i = 0
    PPT = [0,0,0,0,0,0]
    tds = root.cssselect("td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        try:
            if 'POWER PLAYS (Goals-Occurrences / Time)' in td.text or 'POWER PLAYS (Goals-Occurrences/Time)' in td.text:
                PPT[3] = tds[i+7].text
                PPT[4] = tds[i+8].text
                PPT[5] = tds[i+9].text
                PPT[0] = tds[i+16].text
                PPT[1] = tds[i+17].text
                PPT[2] = tds[i+18].text
        except TypeError:
            pass
        i += 1
# PBP data
    i = 0
    goaldiff = 0
    goalstate = 3

    HGEV = [0,0,0,0,0,0,0]
    HSEV = [0,0,0,0,0,0,0]
    HMEV = [0,0,0,0,0,0,0]
    HBEV = [0,0,0,0,0,0,0]
    HPEV = [0,0,0,0,0,0,0]
    AGEV = [0,0,0,0,0,0,0]
    ASEV = [0,0,0,0,0,0,0]
    AMEV = [0,0,0,0,0,0,0]
    ABEV = [0,0,0,0,0,0,0]
    APEV = [0,0,0,0,0,0,0]

    HGPP = [0,0,0,0,0,0,0]
    HSPP = [0,0,0,0,0,0,0]
    HMPP = [0,0,0,0,0,0,0]
    HBPP = [0,0,0,0,0,0,0]
    HPPP = [0,0,0,0,0,0,0]
    AGPP = [0,0,0,0,0,0,0]
    ASPP = [0,0,0,0,0,0,0]
    AMPP = [0,0,0,0,0,0,0]
    ABPP = [0,0,0,0,0,0,0]
    APPP = [0,0,0,0,0,0,0]

    HGSH = [0,0,0,0,0,0,0]
    HSSH = [0,0,0,0,0,0,0]
    HMSH = [0,0,0,0,0,0,0]
    HBSH = [0,0,0,0,0,0,0]
    HPSH = [0,0,0,0,0,0,0]
    AGSH = [0,0,0,0,0,0,0]
    ASSH = [0,0,0,0,0,0,0]
    AMSH = [0,0,0,0,0,0,0]
    ABSH = [0,0,0,0,0,0,0]
    APSH = [0,0,0,0,0,0,0]
    
    time.sleep(3)# delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
        trs = row.cssselect("td")
        if goaldiff > 2:
            goalstate = 6
        elif goaldiff < -2:
            goalstate = 0
        else:
            goalstate = goaldiff + 3
        if ((trs[1].text != "5") and trs[4].text == "GOAL"):
            if (trs[5].text.startswith(hometeam)):
                goaldiff += 1
            else:
                goaldiff -= 1
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HGEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                AGEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HGPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                AGSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HGSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                AGPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT"):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HSEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                ASEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HSPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                ASSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HSSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                ASPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "MISS"):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HMEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                AMEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HMPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                AMSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HMSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                AMPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "BLOCK"):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HBEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                ABEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HBPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                ABSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HBSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                ABPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "PENL") and ('2 min' in trs[5].text):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HPEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                APEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HPPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                APSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HPSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                APPP[int(goalstate)] += 1
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT, PPT, HGEV, HSEV, HMEV, HBEV, HPEV, HGPP, HSPP, HMPP, HBPP, HPPP,HGSH, HSSH, HMSH, HBSH, HPSH, AGEV,ASEV, AMEV, ABEV, APEV, AGPP, ASPP, AMPP, ABPP, APPP,AGSH, ASSH, AMSH, ABSH, APSH]
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
season = 20122013
gidarray = [20074,    20427,    20668]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),20721):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    date = root.cssselect("#GameInfo td")[3].text
    awayscore = root.cssselect("#Visitor td")[3].text
    homescore = root.cssselect("#Home td")[3].text

# scrape_table function: gets passed an individual page to scrape
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
# Get PPTime
    i = 0
    PPT = [0,0,0,0,0,0]
    tds = root.cssselect("td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        try:
            if 'POWER PLAYS (Goals-Occurrences / Time)' in td.text or 'POWER PLAYS (Goals-Occurrences/Time)' in td.text:
                PPT[3] = tds[i+7].text
                PPT[4] = tds[i+8].text
                PPT[5] = tds[i+9].text
                PPT[0] = tds[i+16].text
                PPT[1] = tds[i+17].text
                PPT[2] = tds[i+18].text
        except TypeError:
            pass
        i += 1
# PBP data
    i = 0
    goaldiff = 0
    goalstate = 3

    HGEV = [0,0,0,0,0,0,0]
    HSEV = [0,0,0,0,0,0,0]
    HMEV = [0,0,0,0,0,0,0]
    HBEV = [0,0,0,0,0,0,0]
    HPEV = [0,0,0,0,0,0,0]
    AGEV = [0,0,0,0,0,0,0]
    ASEV = [0,0,0,0,0,0,0]
    AMEV = [0,0,0,0,0,0,0]
    ABEV = [0,0,0,0,0,0,0]
    APEV = [0,0,0,0,0,0,0]

    HGPP = [0,0,0,0,0,0,0]
    HSPP = [0,0,0,0,0,0,0]
    HMPP = [0,0,0,0,0,0,0]
    HBPP = [0,0,0,0,0,0,0]
    HPPP = [0,0,0,0,0,0,0]
    AGPP = [0,0,0,0,0,0,0]
    ASPP = [0,0,0,0,0,0,0]
    AMPP = [0,0,0,0,0,0,0]
    ABPP = [0,0,0,0,0,0,0]
    APPP = [0,0,0,0,0,0,0]

    HGSH = [0,0,0,0,0,0,0]
    HSSH = [0,0,0,0,0,0,0]
    HMSH = [0,0,0,0,0,0,0]
    HBSH = [0,0,0,0,0,0,0]
    HPSH = [0,0,0,0,0,0,0]
    AGSH = [0,0,0,0,0,0,0]
    ASSH = [0,0,0,0,0,0,0]
    AMSH = [0,0,0,0,0,0,0]
    ABSH = [0,0,0,0,0,0,0]
    APSH = [0,0,0,0,0,0,0]
    
    time.sleep(3)# delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
        trs = row.cssselect("td")
        if goaldiff > 2:
            goalstate = 6
        elif goaldiff < -2:
            goalstate = 0
        else:
            goalstate = goaldiff + 3
        if ((trs[1].text != "5") and trs[4].text == "GOAL"):
            if (trs[5].text.startswith(hometeam)):
                goaldiff += 1
            else:
                goaldiff -= 1
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HGEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                AGEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HGPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                AGSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HGSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                AGPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT"):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HSEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                ASEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HSPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                ASSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HSSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                ASPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "MISS"):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HMEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                AMEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HMPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                AMSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HMSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                AMPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "BLOCK"):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HBEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                ABEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HBPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                ABSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HBSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                ABPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "PENL") and ('2 min' in trs[5].text):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HPEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                APEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HPPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                APSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HPSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                APPP[int(goalstate)] += 1
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT, PPT, HGEV, HSEV, HMEV, HBEV, HPEV, HGPP, HSPP, HMPP, HBPP, HPPP,HGSH, HSSH, HMSH, HBSH, HPSH, AGEV,ASEV, AMEV, ABEV, APEV, AGPP, ASPP, AMPP, ABPP, APPP,AGSH, ASSH, AMSH, ABSH, APSH]
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
season = 20122013
gidarray = [20074,    20427,    20668]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),20721):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    date = root.cssselect("#GameInfo td")[3].text
    awayscore = root.cssselect("#Visitor td")[3].text
    homescore = root.cssselect("#Home td")[3].text

# scrape_table function: gets passed an individual page to scrape
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
# Get PPTime
    i = 0
    PPT = [0,0,0,0,0,0]
    tds = root.cssselect("td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        try:
            if 'POWER PLAYS (Goals-Occurrences / Time)' in td.text or 'POWER PLAYS (Goals-Occurrences/Time)' in td.text:
                PPT[3] = tds[i+7].text
                PPT[4] = tds[i+8].text
                PPT[5] = tds[i+9].text
                PPT[0] = tds[i+16].text
                PPT[1] = tds[i+17].text
                PPT[2] = tds[i+18].text
        except TypeError:
            pass
        i += 1
# PBP data
    i = 0
    goaldiff = 0
    goalstate = 3

    HGEV = [0,0,0,0,0,0,0]
    HSEV = [0,0,0,0,0,0,0]
    HMEV = [0,0,0,0,0,0,0]
    HBEV = [0,0,0,0,0,0,0]
    HPEV = [0,0,0,0,0,0,0]
    AGEV = [0,0,0,0,0,0,0]
    ASEV = [0,0,0,0,0,0,0]
    AMEV = [0,0,0,0,0,0,0]
    ABEV = [0,0,0,0,0,0,0]
    APEV = [0,0,0,0,0,0,0]

    HGPP = [0,0,0,0,0,0,0]
    HSPP = [0,0,0,0,0,0,0]
    HMPP = [0,0,0,0,0,0,0]
    HBPP = [0,0,0,0,0,0,0]
    HPPP = [0,0,0,0,0,0,0]
    AGPP = [0,0,0,0,0,0,0]
    ASPP = [0,0,0,0,0,0,0]
    AMPP = [0,0,0,0,0,0,0]
    ABPP = [0,0,0,0,0,0,0]
    APPP = [0,0,0,0,0,0,0]

    HGSH = [0,0,0,0,0,0,0]
    HSSH = [0,0,0,0,0,0,0]
    HMSH = [0,0,0,0,0,0,0]
    HBSH = [0,0,0,0,0,0,0]
    HPSH = [0,0,0,0,0,0,0]
    AGSH = [0,0,0,0,0,0,0]
    ASSH = [0,0,0,0,0,0,0]
    AMSH = [0,0,0,0,0,0,0]
    ABSH = [0,0,0,0,0,0,0]
    APSH = [0,0,0,0,0,0,0]
    
    time.sleep(3)# delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
        trs = row.cssselect("td")
        if goaldiff > 2:
            goalstate = 6
        elif goaldiff < -2:
            goalstate = 0
        else:
            goalstate = goaldiff + 3
        if ((trs[1].text != "5") and trs[4].text == "GOAL"):
            if (trs[5].text.startswith(hometeam)):
                goaldiff += 1
            else:
                goaldiff -= 1
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HGEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                AGEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HGPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                AGSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HGSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                AGPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT"):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HSEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                ASEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HSPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                ASSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HSSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                ASPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "MISS"):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HMEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                AMEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HMPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                AMSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HMSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                AMPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "BLOCK"):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HBEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                ABEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HBPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                ABSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HBSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                ABPP[int(goalstate)] += 1
        elif ((trs[1].text != "5") and trs[4].text == "PENL") and ('2 min' in trs[5].text):
            try:
                arr = []
                hrr = []
                j = j+1
                trs = row.cssselect("table")[0]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                trs = row.cssselect("table")[len(arr)+ 1]
                for tr in trs:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            try:
                awayskate = []
                homeskate = []
                awaycount = 0
                homecount = 0
                i = 9
                trs = row.cssselect("td")
                while i < len(arr)*4+9:
                    awayskate.append(trs[i].text)
                    i += 4
                k = i
                while k < len(hrr)*4+i:
                    homeskate.append(trs[k].text)
                    k += 4
                awaycount = awayskate.count('L') + awayskate.count('C') + awayskate.count('R') + awayskate.count('D') + awayskate.count('G') -1
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (trs[2].text == 'EV'):
                HPEV[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (trs[2].text == 'EV'):
                APEV[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 5 and awaycount == 4):
                HPPP[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 5 and awaycount == 4):
                APSH[int(goalstate)] += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homecount == 4 and awaycount == 5):
                HPSH[int(goalstate)] += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homecount == 4 and awaycount == 5):
                APPP[int(goalstate)] += 1
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT, PPT, HGEV, HSEV, HMEV, HBEV, HPEV, HGPP, HSPP, HMPP, HBPP, HPPP,HGSH, HSSH, HMSH, HBSH, HPSH, AGEV,ASEV, AMEV, ABEV, APEV, AGPP, ASPP, AMPP, ABPP, APPP,AGSH, ASSH, AMSH, ABSH, APSH]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    time.sleep(3) # delay X seconds to throttle URL fetching
