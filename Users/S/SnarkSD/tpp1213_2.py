import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "2012-2013s"
gidarray = [20400]

for gid in range((scraperwiki.sqlite.get_var('gid') + 1),20601):
#for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20122013/GS0" + str(gid) + ".HTM"
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
# Penalty information
    i = 0

    TeamHG2 = 0
    TeamHS2 = 0
    TeamHM2 = 0
    TeamHF2 = 0
    TeamHB2 = 0
    TeamHC2 = 0
    TeamAG2 = 0
    TeamAS2 = 0
    TeamAM2 = 0
    TeamAF2 = 0
    TeamAB2 = 0
    TeamAC2 = 0

    STeamHG2 = 0
    STeamHS2 = 0
    STeamHM2 = 0
    STeamHF2 = 0
    STeamHB2 = 0
    STeamHC2 = 0
    STeamAG2 = 0
    STeamAS2 = 0
    STeamAM2 = 0
    STeamAF2 = 0
    STeamAB2 = 0
    STeamAC2 = 0

    TeamHG1 = 0
    TeamHS1 = 0
    TeamHM1 = 0
    TeamHF1 = 0
    TeamHB1 = 0
    TeamHC1 = 0
    TeamAG1 = 0
    TeamAS1 = 0
    TeamAM1 = 0
    TeamAF1 = 0
    TeamAB1 = 0
    TeamAC1 = 0

    STeamHG1 = 0
    STeamHS1 = 0
    STeamHM1 = 0
    STeamHF1 = 0
    STeamHB1 = 0
    STeamHC1 = 0
    STeamAG1 = 0
    STeamAS1 = 0
    STeamAM1 = 0
    STeamAF1 = 0
    STeamAB1 = 0
    STeamAC1 = 0

    TeamHG0 = 0
    TeamHS0 = 0
    TeamHM0 = 0
    TeamHF0 = 0
    TeamHB0 = 0
    TeamHC0 = 0
    TeamAG0 = 0
    TeamAS0 = 0
    TeamAM0 = 0
    TeamAF0 = 0
    TeamAB0 = 0
    TeamAC0 = 0

    STeamHG0 = 0
    STeamHS0 = 0
    STeamHM0 = 0
    STeamHF0 = 0
    STeamHB0 = 0
    STeamHC0 = 0
    STeamAG0 = 0
    STeamAS0 = 0
    STeamAM0 = 0
    STeamAF0 = 0
    STeamAB0 = 0
    STeamAC0 = 0

    time.sleep(3)# delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/20122013/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
        trs = row.cssselect("td")
        #Power-Play
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHG2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAG2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHG1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAG1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHG0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAG0 += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHS2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAS2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHS1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAS1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHS0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAS0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHM2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAM2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHM1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAM1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHM0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAM0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHB2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAB2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHB1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAB1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHB0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAB0 += 1
        # Short handed
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHG2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAG2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHG1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAG1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHG0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAG0 += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHS2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAS2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHS1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAS1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHS0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAS0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHM2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAM2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHM1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAM1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHM0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAM0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHB2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAB2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHB1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAB1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHB0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAB0 += 1

    TeamHF2 = TeamHG2 + TeamHS2 + TeamHM2
    TeamAF2 = TeamAG2 + TeamAS2 + TeamAM2
    TeamHC2 = TeamHF2 + TeamHB2
    TeamAC2 = TeamAF2 + TeamAB2
    STeamHF2 = STeamHG2 + STeamHS2 + STeamHM2
    STeamAF2 = STeamAG2 + STeamAS2 + STeamAM2
    STeamHC2 = STeamHF2 + STeamHB2
    STeamAC2 = STeamAF2 + STeamAB2

    TeamHF1 = TeamHG1 + TeamHS1 + TeamHM1
    TeamAF1 = TeamAG1 + TeamAS1 + TeamAM1
    TeamHC1 = TeamHF1 + TeamHB1
    TeamAC1 = TeamAF1 + TeamAB1
    STeamHF1 = STeamHG1 + STeamHS1 + STeamHM1
    STeamAF1 = STeamAG1 + STeamAS1 + STeamAM1
    STeamHC1 = STeamHF1 + STeamHB1
    STeamAC1 = STeamAF1 + STeamAB1

    TeamHF0 = TeamHG0 + TeamHS0 + TeamHM0
    TeamAF0 = TeamAG0 + TeamAS0 + TeamAM0
    TeamHC0 = TeamHF0 + TeamHB0
    TeamAC0 = TeamAF0 + TeamAB0
    STeamHF0 = STeamHG0 + STeamHS0 + STeamHM0
    STeamAF0 = STeamAG0 + STeamAS0 + STeamAM0
    STeamHC0 = STeamHF0 + STeamHB0
    STeamAC0 = STeamAF0 + STeamAB0
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT, PPT, [TeamHG2, TeamHS2, TeamHF2, TeamHC2, TeamAG2, TeamAS2, TeamAF2, TeamAC2, STeamHG2, STeamHS2, STeamHF2, STeamHC2, STeamAG2, STeamAS2, STeamAF2, STeamAC2], [TeamHG1, TeamHS1, TeamHF1, TeamHC1, TeamAG1, TeamAS1, TeamAF1, TeamAC1, STeamHG1, STeamHS1, STeamHF1, STeamHC1, STeamAG1, STeamAS1, STeamAF1, STeamAC1], [TeamHG0, TeamHS0, TeamHF0, TeamHC0, TeamAG0, TeamAS0, TeamAF0, TeamAC0, STeamHG0, STeamHS0, STeamHF0, STeamHC0, STeamAG0, STeamAS0, STeamAF0, STeamAC0]]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    #scraperwiki.sqlite.save_var(SOOT, SOOT)
    time.sleep(3) # delay X seconds to throttle URL fetching
import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "2012-2013s"
gidarray = [20400]

for gid in range((scraperwiki.sqlite.get_var('gid') + 1),20601):
#for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20122013/GS0" + str(gid) + ".HTM"
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
# Penalty information
    i = 0

    TeamHG2 = 0
    TeamHS2 = 0
    TeamHM2 = 0
    TeamHF2 = 0
    TeamHB2 = 0
    TeamHC2 = 0
    TeamAG2 = 0
    TeamAS2 = 0
    TeamAM2 = 0
    TeamAF2 = 0
    TeamAB2 = 0
    TeamAC2 = 0

    STeamHG2 = 0
    STeamHS2 = 0
    STeamHM2 = 0
    STeamHF2 = 0
    STeamHB2 = 0
    STeamHC2 = 0
    STeamAG2 = 0
    STeamAS2 = 0
    STeamAM2 = 0
    STeamAF2 = 0
    STeamAB2 = 0
    STeamAC2 = 0

    TeamHG1 = 0
    TeamHS1 = 0
    TeamHM1 = 0
    TeamHF1 = 0
    TeamHB1 = 0
    TeamHC1 = 0
    TeamAG1 = 0
    TeamAS1 = 0
    TeamAM1 = 0
    TeamAF1 = 0
    TeamAB1 = 0
    TeamAC1 = 0

    STeamHG1 = 0
    STeamHS1 = 0
    STeamHM1 = 0
    STeamHF1 = 0
    STeamHB1 = 0
    STeamHC1 = 0
    STeamAG1 = 0
    STeamAS1 = 0
    STeamAM1 = 0
    STeamAF1 = 0
    STeamAB1 = 0
    STeamAC1 = 0

    TeamHG0 = 0
    TeamHS0 = 0
    TeamHM0 = 0
    TeamHF0 = 0
    TeamHB0 = 0
    TeamHC0 = 0
    TeamAG0 = 0
    TeamAS0 = 0
    TeamAM0 = 0
    TeamAF0 = 0
    TeamAB0 = 0
    TeamAC0 = 0

    STeamHG0 = 0
    STeamHS0 = 0
    STeamHM0 = 0
    STeamHF0 = 0
    STeamHB0 = 0
    STeamHC0 = 0
    STeamAG0 = 0
    STeamAS0 = 0
    STeamAM0 = 0
    STeamAF0 = 0
    STeamAB0 = 0
    STeamAC0 = 0

    time.sleep(3)# delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/20122013/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
        trs = row.cssselect("td")
        #Power-Play
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHG2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAG2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHG1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAG1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHG0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAG0 += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHS2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAS2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHS1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAS1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHS0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAS0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHM2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAM2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHM1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAM1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHM0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAM0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHB2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAB2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHB1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAB1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHB0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAB0 += 1
        # Short handed
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHG2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAG2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHG1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAG1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHG0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAG0 += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHS2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAS2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHS1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAS1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHS0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAS0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHM2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAM2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHM1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAM1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHM0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAM0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHB2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAB2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHB1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAB1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHB0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAB0 += 1

    TeamHF2 = TeamHG2 + TeamHS2 + TeamHM2
    TeamAF2 = TeamAG2 + TeamAS2 + TeamAM2
    TeamHC2 = TeamHF2 + TeamHB2
    TeamAC2 = TeamAF2 + TeamAB2
    STeamHF2 = STeamHG2 + STeamHS2 + STeamHM2
    STeamAF2 = STeamAG2 + STeamAS2 + STeamAM2
    STeamHC2 = STeamHF2 + STeamHB2
    STeamAC2 = STeamAF2 + STeamAB2

    TeamHF1 = TeamHG1 + TeamHS1 + TeamHM1
    TeamAF1 = TeamAG1 + TeamAS1 + TeamAM1
    TeamHC1 = TeamHF1 + TeamHB1
    TeamAC1 = TeamAF1 + TeamAB1
    STeamHF1 = STeamHG1 + STeamHS1 + STeamHM1
    STeamAF1 = STeamAG1 + STeamAS1 + STeamAM1
    STeamHC1 = STeamHF1 + STeamHB1
    STeamAC1 = STeamAF1 + STeamAB1

    TeamHF0 = TeamHG0 + TeamHS0 + TeamHM0
    TeamAF0 = TeamAG0 + TeamAS0 + TeamAM0
    TeamHC0 = TeamHF0 + TeamHB0
    TeamAC0 = TeamAF0 + TeamAB0
    STeamHF0 = STeamHG0 + STeamHS0 + STeamHM0
    STeamAF0 = STeamAG0 + STeamAS0 + STeamAM0
    STeamHC0 = STeamHF0 + STeamHB0
    STeamAC0 = STeamAF0 + STeamAB0
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT, PPT, [TeamHG2, TeamHS2, TeamHF2, TeamHC2, TeamAG2, TeamAS2, TeamAF2, TeamAC2, STeamHG2, STeamHS2, STeamHF2, STeamHC2, STeamAG2, STeamAS2, STeamAF2, STeamAC2], [TeamHG1, TeamHS1, TeamHF1, TeamHC1, TeamAG1, TeamAS1, TeamAF1, TeamAC1, STeamHG1, STeamHS1, STeamHF1, STeamHC1, STeamAG1, STeamAS1, STeamAF1, STeamAC1], [TeamHG0, TeamHS0, TeamHF0, TeamHC0, TeamAG0, TeamAS0, TeamAF0, TeamAC0, STeamHG0, STeamHS0, STeamHF0, STeamHC0, STeamAG0, STeamAS0, STeamAF0, STeamAC0]]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    #scraperwiki.sqlite.save_var(SOOT, SOOT)
    time.sleep(3) # delay X seconds to throttle URL fetching
import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "2012-2013s"
gidarray = [20400]

for gid in range((scraperwiki.sqlite.get_var('gid') + 1),20601):
#for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20122013/GS0" + str(gid) + ".HTM"
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
# Penalty information
    i = 0

    TeamHG2 = 0
    TeamHS2 = 0
    TeamHM2 = 0
    TeamHF2 = 0
    TeamHB2 = 0
    TeamHC2 = 0
    TeamAG2 = 0
    TeamAS2 = 0
    TeamAM2 = 0
    TeamAF2 = 0
    TeamAB2 = 0
    TeamAC2 = 0

    STeamHG2 = 0
    STeamHS2 = 0
    STeamHM2 = 0
    STeamHF2 = 0
    STeamHB2 = 0
    STeamHC2 = 0
    STeamAG2 = 0
    STeamAS2 = 0
    STeamAM2 = 0
    STeamAF2 = 0
    STeamAB2 = 0
    STeamAC2 = 0

    TeamHG1 = 0
    TeamHS1 = 0
    TeamHM1 = 0
    TeamHF1 = 0
    TeamHB1 = 0
    TeamHC1 = 0
    TeamAG1 = 0
    TeamAS1 = 0
    TeamAM1 = 0
    TeamAF1 = 0
    TeamAB1 = 0
    TeamAC1 = 0

    STeamHG1 = 0
    STeamHS1 = 0
    STeamHM1 = 0
    STeamHF1 = 0
    STeamHB1 = 0
    STeamHC1 = 0
    STeamAG1 = 0
    STeamAS1 = 0
    STeamAM1 = 0
    STeamAF1 = 0
    STeamAB1 = 0
    STeamAC1 = 0

    TeamHG0 = 0
    TeamHS0 = 0
    TeamHM0 = 0
    TeamHF0 = 0
    TeamHB0 = 0
    TeamHC0 = 0
    TeamAG0 = 0
    TeamAS0 = 0
    TeamAM0 = 0
    TeamAF0 = 0
    TeamAB0 = 0
    TeamAC0 = 0

    STeamHG0 = 0
    STeamHS0 = 0
    STeamHM0 = 0
    STeamHF0 = 0
    STeamHB0 = 0
    STeamHC0 = 0
    STeamAG0 = 0
    STeamAS0 = 0
    STeamAM0 = 0
    STeamAF0 = 0
    STeamAB0 = 0
    STeamAC0 = 0

    time.sleep(3)# delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/20122013/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
        trs = row.cssselect("td")
        #Power-Play
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHG2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAG2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHG1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAG1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHG0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAG0 += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHS2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAS2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHS1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAS1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHS0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAS0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHM2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAM2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHM1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAM1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHM0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAM0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHB2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAB2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHB1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAB1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHB0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAB0 += 1
        # Short handed
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHG2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAG2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHG1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAG1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHG0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAG0 += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHS2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAS2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHS1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAS1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHS0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAS0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHM2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAM2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHM1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAM1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHM0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAM0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHB2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAB2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHB1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAB1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHB0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAB0 += 1

    TeamHF2 = TeamHG2 + TeamHS2 + TeamHM2
    TeamAF2 = TeamAG2 + TeamAS2 + TeamAM2
    TeamHC2 = TeamHF2 + TeamHB2
    TeamAC2 = TeamAF2 + TeamAB2
    STeamHF2 = STeamHG2 + STeamHS2 + STeamHM2
    STeamAF2 = STeamAG2 + STeamAS2 + STeamAM2
    STeamHC2 = STeamHF2 + STeamHB2
    STeamAC2 = STeamAF2 + STeamAB2

    TeamHF1 = TeamHG1 + TeamHS1 + TeamHM1
    TeamAF1 = TeamAG1 + TeamAS1 + TeamAM1
    TeamHC1 = TeamHF1 + TeamHB1
    TeamAC1 = TeamAF1 + TeamAB1
    STeamHF1 = STeamHG1 + STeamHS1 + STeamHM1
    STeamAF1 = STeamAG1 + STeamAS1 + STeamAM1
    STeamHC1 = STeamHF1 + STeamHB1
    STeamAC1 = STeamAF1 + STeamAB1

    TeamHF0 = TeamHG0 + TeamHS0 + TeamHM0
    TeamAF0 = TeamAG0 + TeamAS0 + TeamAM0
    TeamHC0 = TeamHF0 + TeamHB0
    TeamAC0 = TeamAF0 + TeamAB0
    STeamHF0 = STeamHG0 + STeamHS0 + STeamHM0
    STeamAF0 = STeamAG0 + STeamAS0 + STeamAM0
    STeamHC0 = STeamHF0 + STeamHB0
    STeamAC0 = STeamAF0 + STeamAB0
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT, PPT, [TeamHG2, TeamHS2, TeamHF2, TeamHC2, TeamAG2, TeamAS2, TeamAF2, TeamAC2, STeamHG2, STeamHS2, STeamHF2, STeamHC2, STeamAG2, STeamAS2, STeamAF2, STeamAC2], [TeamHG1, TeamHS1, TeamHF1, TeamHC1, TeamAG1, TeamAS1, TeamAF1, TeamAC1, STeamHG1, STeamHS1, STeamHF1, STeamHC1, STeamAG1, STeamAS1, STeamAF1, STeamAC1], [TeamHG0, TeamHS0, TeamHF0, TeamHC0, TeamAG0, TeamAS0, TeamAF0, TeamAC0, STeamHG0, STeamHS0, STeamHF0, STeamHC0, STeamAG0, STeamAS0, STeamAF0, STeamAC0]]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    #scraperwiki.sqlite.save_var(SOOT, SOOT)
    time.sleep(3) # delay X seconds to throttle URL fetching
import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "2012-2013s"
gidarray = [20400]

for gid in range((scraperwiki.sqlite.get_var('gid') + 1),20601):
#for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20122013/GS0" + str(gid) + ".HTM"
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
# Penalty information
    i = 0

    TeamHG2 = 0
    TeamHS2 = 0
    TeamHM2 = 0
    TeamHF2 = 0
    TeamHB2 = 0
    TeamHC2 = 0
    TeamAG2 = 0
    TeamAS2 = 0
    TeamAM2 = 0
    TeamAF2 = 0
    TeamAB2 = 0
    TeamAC2 = 0

    STeamHG2 = 0
    STeamHS2 = 0
    STeamHM2 = 0
    STeamHF2 = 0
    STeamHB2 = 0
    STeamHC2 = 0
    STeamAG2 = 0
    STeamAS2 = 0
    STeamAM2 = 0
    STeamAF2 = 0
    STeamAB2 = 0
    STeamAC2 = 0

    TeamHG1 = 0
    TeamHS1 = 0
    TeamHM1 = 0
    TeamHF1 = 0
    TeamHB1 = 0
    TeamHC1 = 0
    TeamAG1 = 0
    TeamAS1 = 0
    TeamAM1 = 0
    TeamAF1 = 0
    TeamAB1 = 0
    TeamAC1 = 0

    STeamHG1 = 0
    STeamHS1 = 0
    STeamHM1 = 0
    STeamHF1 = 0
    STeamHB1 = 0
    STeamHC1 = 0
    STeamAG1 = 0
    STeamAS1 = 0
    STeamAM1 = 0
    STeamAF1 = 0
    STeamAB1 = 0
    STeamAC1 = 0

    TeamHG0 = 0
    TeamHS0 = 0
    TeamHM0 = 0
    TeamHF0 = 0
    TeamHB0 = 0
    TeamHC0 = 0
    TeamAG0 = 0
    TeamAS0 = 0
    TeamAM0 = 0
    TeamAF0 = 0
    TeamAB0 = 0
    TeamAC0 = 0

    STeamHG0 = 0
    STeamHS0 = 0
    STeamHM0 = 0
    STeamHF0 = 0
    STeamHB0 = 0
    STeamHC0 = 0
    STeamAG0 = 0
    STeamAS0 = 0
    STeamAM0 = 0
    STeamAF0 = 0
    STeamAB0 = 0
    STeamAC0 = 0

    time.sleep(3)# delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/20122013/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
        trs = row.cssselect("td")
        #Power-Play
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHG2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAG2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHG1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAG1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHG0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAG0 += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHS2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAS2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHS1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAS1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHS0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAS0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHM2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAM2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHM1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAM1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHM0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAM0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                TeamHB2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                TeamAB2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                TeamHB1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                TeamAB1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                TeamHB0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                TeamAB0 += 1
        # Short handed
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHG2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAG2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHG1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAG1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHG0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAG0 += 1
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHS2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAS2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHS1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAS1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHS0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAS0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "SH"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHM2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAM2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHM1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAM1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHM0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAM0 += 1
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "PP"):
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
                awayDcount = 0
                homecount = 0
                homeDcount = 0
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
                awayDcount = awayskate.count('D')
                homecount = homeskate.count('L') + homeskate.count('C') + homeskate.count('R') + homeskate.count('D') + homeskate.count('G') - 1
                homeDcount = homeskate.count('D')
            except IndexError:
                pass
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 2) and (homecount == 4) and (awaycount == 5):
                STeamHB2 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 2) and (homecount == 5) and (awaycount == 4):
                STeamAB2 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 1) and (homecount == 4) and (awaycount == 5):
                STeamHB1 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 1) and (homecount == 5) and (awaycount == 4):
                STeamAB1 += 1
            if ('G' in awayskate and 'G' in homeskate) and (trs[5].text.startswith(hometeam)) and (awayDcount == 0) and (homecount == 4) and (awaycount == 5):
                STeamHB0 += 1
            elif ('G' in awayskate and 'G' in homeskate) and (homeDcount == 0) and (homecount == 5) and (awaycount == 4):
                STeamAB0 += 1

    TeamHF2 = TeamHG2 + TeamHS2 + TeamHM2
    TeamAF2 = TeamAG2 + TeamAS2 + TeamAM2
    TeamHC2 = TeamHF2 + TeamHB2
    TeamAC2 = TeamAF2 + TeamAB2
    STeamHF2 = STeamHG2 + STeamHS2 + STeamHM2
    STeamAF2 = STeamAG2 + STeamAS2 + STeamAM2
    STeamHC2 = STeamHF2 + STeamHB2
    STeamAC2 = STeamAF2 + STeamAB2

    TeamHF1 = TeamHG1 + TeamHS1 + TeamHM1
    TeamAF1 = TeamAG1 + TeamAS1 + TeamAM1
    TeamHC1 = TeamHF1 + TeamHB1
    TeamAC1 = TeamAF1 + TeamAB1
    STeamHF1 = STeamHG1 + STeamHS1 + STeamHM1
    STeamAF1 = STeamAG1 + STeamAS1 + STeamAM1
    STeamHC1 = STeamHF1 + STeamHB1
    STeamAC1 = STeamAF1 + STeamAB1

    TeamHF0 = TeamHG0 + TeamHS0 + TeamHM0
    TeamAF0 = TeamAG0 + TeamAS0 + TeamAM0
    TeamHC0 = TeamHF0 + TeamHB0
    TeamAC0 = TeamAF0 + TeamAB0
    STeamHF0 = STeamHG0 + STeamHS0 + STeamHM0
    STeamAF0 = STeamAG0 + STeamAS0 + STeamAM0
    STeamHC0 = STeamHF0 + STeamHB0
    STeamAC0 = STeamAF0 + STeamAB0
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT, PPT, [TeamHG2, TeamHS2, TeamHF2, TeamHC2, TeamAG2, TeamAS2, TeamAF2, TeamAC2, STeamHG2, STeamHS2, STeamHF2, STeamHC2, STeamAG2, STeamAS2, STeamAF2, STeamAC2], [TeamHG1, TeamHS1, TeamHF1, TeamHC1, TeamAG1, TeamAS1, TeamAF1, TeamAC1, STeamHG1, STeamHS1, STeamHF1, STeamHC1, STeamAG1, STeamAS1, STeamAF1, STeamAC1], [TeamHG0, TeamHS0, TeamHF0, TeamHC0, TeamAG0, TeamAS0, TeamAF0, TeamAC0, STeamHG0, STeamHS0, STeamHF0, STeamHC0, STeamAG0, STeamAS0, STeamAF0, STeamAC0]]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    #scraperwiki.sqlite.save_var(SOOT, SOOT)
    time.sleep(3) # delay X seconds to throttle URL fetching
