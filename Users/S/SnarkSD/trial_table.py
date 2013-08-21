import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = 0
j = 0
season = "2012-2013s"
gidarray = [20004]

for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20122013/PL0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    rows= root.cssselect("tr.evenColor")
    for row in rows:
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
            darr = []
            dhrr = []
            line = []
            i = 9
            trs = row.cssselect("td")
            while i < len(arr)*4+9:
                darr.append(trs[i].text)
                i += 4
            k = i
            while k < len(hrr)*4+i:
                dhrr.append(trs[k].text)
                k += 4
            print j, arr, hrr, darr, dhrr
            print trs[1].text, trs[2].text, trs[4].text
            #for td in trs:
            #    line.append(td.text)
            print line
        except IndexError:
            pass
