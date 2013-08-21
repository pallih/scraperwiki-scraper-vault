import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

gameurlstart = "http://www.nhl.com/scores/htmlreports/20112012/PL0"
gameurlend = ".HTM"

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
gidarray = [21035,    21044,    21096,    21153,    21160,    21196,    21214]

for gid in gidarray: #range((scraperwiki.sqlite.get_var('gid') + 1),(scraperwiki.sqlite.get_var('gid') + 6)):
    if gid < 10:
        url = gameurlstart + "000" + str(gid) + gameurlend
    elif gid < 100:
        url = gameurlstart + "00" + str(gid) + gameurlend
    elif gid <1000:
        url = gameurlstart + "0" + str(gid) + gameurlend
    else:
        url = gameurlstart + str(gid) + gameurlend

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    scraperwiki.sqlite.save_var('gid', gid)
    
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]

    k = i = starttime = event = face = 0
    SJhomeC = range(100)
    SJhomeS = range(100)
    SJawayC = range(100)
    homeCorsiF = [0,0,0,0,0,0]
    homeCorsiA = [0,0,0,0,0,0]
    shift = [0,0,0,0,0,0]
    save = [0, 0, 0, 0, 0, 0]
    m = -1
    for player in range(100):
        SJhomeC[player] = [0,0,0,0,0,0]
        SJawayC[player] = [0,0,0,0,0,0]
        SJhomeS[player] = [0,0,0,0,0,0]

    tds = root.cssselect("tr.evenColor td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if tds[i - 2].text == "EV" and (td.text == "FAC") and int(tds[i - 3].text) < 4:
                faceline = range(13)
                x = 0
                m = i + 4
                while x < 14:
                    tdsContents = tds[m].findall("font")
                    for content in tdsContents:
                        faceline[x] = int(content.text)
                    x += 1
                    m += 4
                if tds[i + 1].text.startswith(hometeam) and ("Off." in tds[i + 1].text):
                    face = 0
                    shift[0] += 1
                elif tds[i + 1].text.startswith(hometeam) and ("Neu." in tds[i + 1].text):
                    face = 1
                    shift[1] += 1
                elif tds[i + 1].text.startswith(hometeam) and ("Def." in tds[i + 1].text):
                    face = 2
                    shift[2] += 1
                elif tds[i + 1].text.startswith(awayteam) and ("Off." in tds[i + 1].text):
                    face = 3
                    shift[3] += 1
                elif tds[i + 1].text.startswith(awayteam) and ("Neu." in tds[i + 1].text):
                    face = 4
                    shift[4] += 1
                elif tds[i + 1].text.startswith(awayteam) and ("Def." in tds[i + 1].text):
                    face = 5
                    shift[5] += 1
                player = range(100)
                for player in faceline[0:6]:
                    SJhomeS[player][face] += 1
        if tds[i - 2].text == "EV" and (td.text == "GOAL") and int(tds[i - 3].text) < 4 or tds[i - 2].text == "EV" and (td.text == "SHOT") and int(tds[i - 3].text) < 4 or tds[i - 2].text == "EV" and (td.text == "MISS") and int(tds[i - 3].text) < 4 or tds[i - 2].text == "EV" and (td.text == "BLOCK") and int(tds[i - 3].text) < 4:
            eventline = range(13)
            x = 0
            m = i + 4
            while x < 14:
                tdsContents = tds[m].findall("font")
                for content in tdsContents:
                    eventline[x] = int(content.text)
                x += 1
                m += 4
            if faceline == eventline:       
                if tds[i + 1].text.startswith(hometeam):
                    homeCorsiF[face] += 1 #increment corsi for by 1 for specific zone
                    for jump in eventline[0:6]:
                        SJhomeC[jump][face] += 1
                        #print tds[i - 3].text, tds[i - 2].text, tds[i - 1].text, "for", jump, face, SJhomeC[jump][face], SJhomeC[jump]
                elif tds[i + 1].text.startswith(awayteam):
                    homeCorsiA[face] += 1
                    for marker in eventline[0:6]:
                        SJawayC[marker][face] += 1
                        #print tds[i - 3].text, tds[i - 2].text, tds[i - 1].text, "against", marker, face, SJawayC[marker][face], SJawayC[marker]
        i += 1
    save = ["v2", gid, hometeam, awayteam, homeCorsiF, homeCorsiA, SJhomeC, SJawayC, SJhomeS]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    j += 1
    time.sleep(3) # delay X seconds to throttle URL fetching
import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

gameurlstart = "http://www.nhl.com/scores/htmlreports/20112012/PL0"
gameurlend = ".HTM"

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
gidarray = [21035,    21044,    21096,    21153,    21160,    21196,    21214]

for gid in gidarray: #range((scraperwiki.sqlite.get_var('gid') + 1),(scraperwiki.sqlite.get_var('gid') + 6)):
    if gid < 10:
        url = gameurlstart + "000" + str(gid) + gameurlend
    elif gid < 100:
        url = gameurlstart + "00" + str(gid) + gameurlend
    elif gid <1000:
        url = gameurlstart + "0" + str(gid) + gameurlend
    else:
        url = gameurlstart + str(gid) + gameurlend

    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    scraperwiki.sqlite.save_var('gid', gid)
    
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]

    k = i = starttime = event = face = 0
    SJhomeC = range(100)
    SJhomeS = range(100)
    SJawayC = range(100)
    homeCorsiF = [0,0,0,0,0,0]
    homeCorsiA = [0,0,0,0,0,0]
    shift = [0,0,0,0,0,0]
    save = [0, 0, 0, 0, 0, 0]
    m = -1
    for player in range(100):
        SJhomeC[player] = [0,0,0,0,0,0]
        SJawayC[player] = [0,0,0,0,0,0]
        SJhomeS[player] = [0,0,0,0,0,0]

    tds = root.cssselect("tr.evenColor td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if tds[i - 2].text == "EV" and (td.text == "FAC") and int(tds[i - 3].text) < 4:
                faceline = range(13)
                x = 0
                m = i + 4
                while x < 14:
                    tdsContents = tds[m].findall("font")
                    for content in tdsContents:
                        faceline[x] = int(content.text)
                    x += 1
                    m += 4
                if tds[i + 1].text.startswith(hometeam) and ("Off." in tds[i + 1].text):
                    face = 0
                    shift[0] += 1
                elif tds[i + 1].text.startswith(hometeam) and ("Neu." in tds[i + 1].text):
                    face = 1
                    shift[1] += 1
                elif tds[i + 1].text.startswith(hometeam) and ("Def." in tds[i + 1].text):
                    face = 2
                    shift[2] += 1
                elif tds[i + 1].text.startswith(awayteam) and ("Off." in tds[i + 1].text):
                    face = 3
                    shift[3] += 1
                elif tds[i + 1].text.startswith(awayteam) and ("Neu." in tds[i + 1].text):
                    face = 4
                    shift[4] += 1
                elif tds[i + 1].text.startswith(awayteam) and ("Def." in tds[i + 1].text):
                    face = 5
                    shift[5] += 1
                player = range(100)
                for player in faceline[0:6]:
                    SJhomeS[player][face] += 1
        if tds[i - 2].text == "EV" and (td.text == "GOAL") and int(tds[i - 3].text) < 4 or tds[i - 2].text == "EV" and (td.text == "SHOT") and int(tds[i - 3].text) < 4 or tds[i - 2].text == "EV" and (td.text == "MISS") and int(tds[i - 3].text) < 4 or tds[i - 2].text == "EV" and (td.text == "BLOCK") and int(tds[i - 3].text) < 4:
            eventline = range(13)
            x = 0
            m = i + 4
            while x < 14:
                tdsContents = tds[m].findall("font")
                for content in tdsContents:
                    eventline[x] = int(content.text)
                x += 1
                m += 4
            if faceline == eventline:       
                if tds[i + 1].text.startswith(hometeam):
                    homeCorsiF[face] += 1 #increment corsi for by 1 for specific zone
                    for jump in eventline[0:6]:
                        SJhomeC[jump][face] += 1
                        #print tds[i - 3].text, tds[i - 2].text, tds[i - 1].text, "for", jump, face, SJhomeC[jump][face], SJhomeC[jump]
                elif tds[i + 1].text.startswith(awayteam):
                    homeCorsiA[face] += 1
                    for marker in eventline[0:6]:
                        SJawayC[marker][face] += 1
                        #print tds[i - 3].text, tds[i - 2].text, tds[i - 1].text, "against", marker, face, SJawayC[marker][face], SJawayC[marker]
        i += 1
    save = ["v2", gid, hometeam, awayteam, homeCorsiF, homeCorsiA, SJhomeC, SJawayC, SJhomeS]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    j += 1
    time.sleep(3) # delay X seconds to throttle URL fetching
