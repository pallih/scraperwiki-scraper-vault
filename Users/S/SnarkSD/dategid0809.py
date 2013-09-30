import scraperwiki
import lxml.etree
import lxml.html
import datetime
import time

teamidlong = ["ANAHEIM DUCKS", "BOSTON BRUINS", "BUFFALO SABRES", "CALGARY FLAMES",  "CAROLINA HURRICANES",  "CHICAGO BLACKHAWKS",  "COLORADO AVALANCHE", "COLUMBUS BLUE JACKETS",  "DALLAS STARS", "DETROIT RED WINGS", "EDMONTON OILERS", "FLORIDA PANTHERS", "LOS ANGELES KINGS", "MINNESOTA WILD", "MONTREAL CANADIENS", "NASHVILLE PREDATORS", "NEW JERSEY DEVILS", "NEW YORK ISLANDERS", "NEW YORK RANGERS", "OTTAWA SENATORS", "PHILADELPHIA FLYERS", "PHOENIX COYOTES", "PITTSBURGH PENGUINS", "SAN JOSE SHARKS", "ST. LOUIS BLUES", "TAMPA BAY LIGHTNING", "TORONTO MAPLE LEAFS", "VANCOUVER CANUCKS", "WASHINGTON CAPITALS", "WINNIPEG JETS", "ATLANTA THRASHERS", "CANADIENS MONTREAL"]

teamid = ["ANA", "BOS", "BUF", "CGY",  "CAR",  "CHI",  "COL", "CBJ",  "DAL", "DET", "EDM", "FLA", "L.A", "MIN", "MTL", "NSH", "N.J", "NYI", "NYR", "OTT", "PHI", "PHX", "PIT", "S.J", "STL", "T.B", "TOR", "VAN", "WSH", "WPG", "ATL", "MTL"]
gid = j = 0
season = "2008-2009s"
gidarray = [20015,    20026,    20502,    20582,    20665]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21231):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20082009/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    SOOT = 0
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    date = root.cssselect("#GameInfo td")[3].text
    awayscore = root.cssselect("#Visitor td")[3].text
    homescore = root.cssselect("#Home td")[3].text

# scrape_table function: gets passed an individual page to scrape
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        table_cells = row.cssselect("td")
        if table_cells:
            if "OT" in table_cells[1].text:
                SOOT = 1
            elif "SO" in table_cells[1].text:
                SOOT = 2
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT]
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
season = "2008-2009s"
gidarray = [20015,    20026,    20502,    20582,    20665]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21231):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20082009/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    SOOT = 0
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    date = root.cssselect("#GameInfo td")[3].text
    awayscore = root.cssselect("#Visitor td")[3].text
    homescore = root.cssselect("#Home td")[3].text

# scrape_table function: gets passed an individual page to scrape
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        table_cells = row.cssselect("td")
        if table_cells:
            if "OT" in table_cells[1].text:
                SOOT = 1
            elif "SO" in table_cells[1].text:
                SOOT = 2
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT]
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
season = "2008-2009s"
gidarray = [20015,    20026,    20502,    20582,    20665]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21231):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20082009/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    SOOT = 0
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    date = root.cssselect("#GameInfo td")[3].text
    awayscore = root.cssselect("#Visitor td")[3].text
    homescore = root.cssselect("#Home td")[3].text

# scrape_table function: gets passed an individual page to scrape
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        table_cells = row.cssselect("td")
        if table_cells:
            if "OT" in table_cells[1].text:
                SOOT = 1
            elif "SO" in table_cells[1].text:
                SOOT = 2
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT]
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
season = "2008-2009s"
gidarray = [20015,    20026,    20502,    20582,    20665]

#for gid in range((scraperwiki.sqlite.get_var('gid') + 1),21231):
for gid in gidarray:
    scraperwiki.sqlite.save_var('gid', gid)
    url = "http://www.nhl.com/scores/htmlreports/20082009/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    SOOT = 0
    awayteam = teamid[teamidlong.index(root.cssselect("#Visitor td")[5].text)] # Matches the contents of the 5th <td> in the html element with id "Visitor" to short awayteam
    hometeam = teamid[teamidlong.index(root.cssselect("#Home td")[5].text)]
    date = root.cssselect("#GameInfo td")[3].text
    awayscore = root.cssselect("#Visitor td")[3].text
    homescore = root.cssselect("#Home td")[3].text

# scrape_table function: gets passed an individual page to scrape
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    for row in rows:
        table_cells = row.cssselect("td")
        if table_cells:
            if "OT" in table_cells[1].text:
                SOOT = 1
            elif "SO" in table_cells[1].text:
                SOOT = 2
    save = [season, gid, date, hometeam, homescore, awayteam, awayscore, SOOT]
    print save
    scraperwiki.sqlite.save_var(gid, save)
    time.sleep(3) # delay X seconds to throttle URL fetching   
