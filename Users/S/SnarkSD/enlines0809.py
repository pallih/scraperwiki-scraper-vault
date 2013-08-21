import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

gameurlstart = "http://www.nhl.com/scores/htmlreports/20082009/PL02"
gameurlend = ".HTM"

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "2008-2009s"
gidarray = [1078]

for gid in range((scraperwiki.sqlite.get_var('gid') + 1),(scraperwiki.sqlite.get_var('gid') + 1230)):
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
    HEN = []
    AEN = []    
    i = 0

    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]

    tds = root.cssselect("tr.evenColor td") # assign all <td> elements of PBP data only to a list called "tds"
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if (tds[i-3].text != "5") and td.text =="GOAL" or td.text =="SHOT" or td.text =="MISS" or td.text =="BLOCK" or td.text =="PENL" or td.text =="FAC" or td.text =="GIVE" or td.text =="HIT" or td.text =="TAKE" or td.text =="STOP":
            #print i, td.text, tds[i-4].text
            try:
                awayskate = (tds[i+5].text,tds[i+9].text,tds[i+13].text,tds[i+17].text,tds[i+21].text,tds[i+25].text)
            except IndexError:
                pass
            if 'G' in awayskate:
                pass
            else:
                AEN.append(tds[i-4].text)
            try:
                homeskate = ([tds[i+29].text,tds[i+33].text,tds[i+37].text,tds[i+41].text,tds[i+45].text,tds[i+49].text])
            except IndexError:
                pass
            if 'G' in homeskate:
                pass
            else:
                HEN.append(tds[i-4].text)
        i += 1
    save = [season, gid, hometeam, awayteam, HEN, AEN]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    scraperwiki.sqlite.save_var('gid', gid)
    j += 1
    time.sleep(3) # delay X seconds to throttle URL fetching
