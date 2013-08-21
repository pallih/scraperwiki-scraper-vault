import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "20082009"
gidarray = [20247,    20496,    20644,    20889,    21136]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21231):
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

#Scrape Goalie Roster info
    HG1 = HG2 = AG1 = AG2 = []
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/RO0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    tables = root.cssselect("table")[11]
    tds = tables[len(tables)-1].cssselect("td")
    HG1 = [tds[0].text, tds[2].text]
    tds = tables[len(tables)-2].cssselect("td")
    HG2 = [tds[0].text, tds[2].text]
    tables = root.cssselect("table")[10]
    tds = tables[len(tables)-1].cssselect("td")
    AG1 = [tds[0].text, tds[2].text]
    tds = tables[len(tables)-2].cssselect("td")
    AG2 = [tds[0].text, tds[2].text]

#Scrape Goalie Save info
    i = 0
    G = [[]] * 4
    G[0] = [0,0,0,0]
    G[1] = [0,0,0,0]
    G[2] = [0,0,0,0]
    G[3] = [0,0,0,0]

    time.sleep(3)# delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
        trs = row.cssselect("td")
        #5v5 Even-Strength excluding empty net
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "EV"):
            try: 
                arr = []
                hrr = []
                j = j+1
                tas = row.cssselect("table")[0]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                tas = row.cssselect("table")[len(arr)+ 1]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            if len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(hometeam)):
                if (AG1[0] in arr) and (HG1[0] in hrr) or (HG2[0] in hrr):
                    G[2][0] += 1
                elif (AG2[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[3][0] += 1
            elif len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(awayteam)):
                if (HG1[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[0][0] += 1
                elif (HG2[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[1][0] += 1           
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "EV"):
            try: 
                arr = []
                hrr = []
                j = j+1
                tas = row.cssselect("table")[0]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                tas = row.cssselect("table")[len(arr)+ 1]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            if (len(arr) == 6) and (len(hrr) == 6) and (trs[5].text.startswith(hometeam)):
                if (AG1[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[2][1] += 1
                elif (AG2[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[3][1] += 1
            elif len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(awayteam)):
                if (HG1[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[0][1] += 1
                elif (HG2[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[1][1] += 1   
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "EV"):
            try: 
                arr = []
                hrr = []
                j = j+1
                tas = row.cssselect("table")[0]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                tas = row.cssselect("table")[len(arr)+ 1]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            if len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(hometeam)):
                if (AG1[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[2][2] += 1
                elif (AG2[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[3][2] += 1
            elif len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(awayteam)):
                if (HG1[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[0][2] += 1
                elif (HG2[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[1][2] += 1   
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "EV"):
            try: 
                arr = []
                hrr = []
                j = j+1
                tas = row.cssselect("table")[0]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                tas = row.cssselect("table")[len(arr)+ 1]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            if len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(hometeam)):
                if (AG1[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[2][3] =+ 1
                elif (AG2[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[3][3] =+ 1
            elif len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(awayteam)):
                if (HG1[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[0][3] =+ 1
                elif (HG2[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[1][3] =+ 1
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT, HG1, HG2, AG1, AG2, G]
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
season = "20082009"
gidarray = [20247,    20496,    20644,    20889,    21136]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21231):
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

#Scrape Goalie Roster info
    HG1 = HG2 = AG1 = AG2 = []
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/RO0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    tables = root.cssselect("table")[11]
    tds = tables[len(tables)-1].cssselect("td")
    HG1 = [tds[0].text, tds[2].text]
    tds = tables[len(tables)-2].cssselect("td")
    HG2 = [tds[0].text, tds[2].text]
    tables = root.cssselect("table")[10]
    tds = tables[len(tables)-1].cssselect("td")
    AG1 = [tds[0].text, tds[2].text]
    tds = tables[len(tables)-2].cssselect("td")
    AG2 = [tds[0].text, tds[2].text]

#Scrape Goalie Save info
    i = 0
    G = [[]] * 4
    G[0] = [0,0,0,0]
    G[1] = [0,0,0,0]
    G[2] = [0,0,0,0]
    G[3] = [0,0,0,0]

    time.sleep(3)# delay X seconds to throttle URL fetching  
    url = "http://www.nhl.com/scores/htmlreports/" + str(season) + "/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
        trs = row.cssselect("td")
        #5v5 Even-Strength excluding empty net
        if ((trs[1].text != "5") and trs[4].text == "GOAL") and (trs[2].text == "EV"):
            try: 
                arr = []
                hrr = []
                j = j+1
                tas = row.cssselect("table")[0]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                tas = row.cssselect("table")[len(arr)+ 1]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            if len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(hometeam)):
                if (AG1[0] in arr) and (HG1[0] in hrr) or (HG2[0] in hrr):
                    G[2][0] += 1
                elif (AG2[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[3][0] += 1
            elif len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(awayteam)):
                if (HG1[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[0][0] += 1
                elif (HG2[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[1][0] += 1           
        elif ((trs[1].text != "5") and trs[4].text == "SHOT")  and (trs[2].text == "EV"):
            try: 
                arr = []
                hrr = []
                j = j+1
                tas = row.cssselect("table")[0]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                tas = row.cssselect("table")[len(arr)+ 1]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            if (len(arr) == 6) and (len(hrr) == 6) and (trs[5].text.startswith(hometeam)):
                if (AG1[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[2][1] += 1
                elif (AG2[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[3][1] += 1
            elif len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(awayteam)):
                if (HG1[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[0][1] += 1
                elif (HG2[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[1][1] += 1   
        elif ((trs[1].text != "5") and trs[4].text =="MISS")  and (trs[2].text == "EV"):
            try: 
                arr = []
                hrr = []
                j = j+1
                tas = row.cssselect("table")[0]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                tas = row.cssselect("table")[len(arr)+ 1]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            if len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(hometeam)):
                if (AG1[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[2][2] += 1
                elif (AG2[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[3][2] += 1
            elif len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(awayteam)):
                if (HG1[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[0][2] += 1
                elif (HG2[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[1][2] += 1   
        elif ((trs[1].text != "5") and trs[4].text =="BLOCK")  and (trs[2].text == "EV"):
            try: 
                arr = []
                hrr = []
                j = j+1
                tas = row.cssselect("table")[0]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        arr.append(td.text)
                tas = row.cssselect("table")[len(arr)+ 1]
                for tr in tas:
                    tds = tr.cssselect("font")
                    for td in tds:
                        hrr.append(td.text)
            except IndexError:
                pass
            if len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(hometeam)):
                if (AG1[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[2][3] =+ 1
                elif (AG2[0] in arr) and (HG1[0] in hrr or HG2[0] in hrr):
                    G[3][3] =+ 1
            elif len(arr) == 6 and len(hrr) == 6 and (trs[5].text.startswith(awayteam)):
                if (HG1[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[0][3] =+ 1
                elif (HG2[0] in hrr) and (AG1[0] in arr or AG2[0] in arr):
                    G[1][3] =+ 1
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT, HG1, HG2, AG1, AG2, G]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    #scraperwiki.sqlite.save_var(SOOT, SOOT)
    time.sleep(3) # delay X seconds to throttle URL fetching   
