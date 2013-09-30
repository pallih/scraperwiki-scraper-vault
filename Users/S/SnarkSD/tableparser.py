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
    url = "http://www.nhl.com/scores/htmlreports/20112012/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object

# scrape_table function: gets passed an individual page to scrape
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    n = 1
    for row in rows:
        # Set up our data record - we'll need it later 
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['gid'] = gid
            record['Goal'] = table_cells[0].text
            record['Per'] = table_cells[1].text
            record['Time'] = table_cells[2].text
            record['Str'] = table_cells[3].text
            record['Team'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            n += 1
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save_var('record', record)
    #scraperwiki.sqlite.save_var(gid, save)
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
    url = "http://www.nhl.com/scores/htmlreports/20112012/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object

# scrape_table function: gets passed an individual page to scrape
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    n = 1
    for row in rows:
        # Set up our data record - we'll need it later 
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['gid'] = gid
            record['Goal'] = table_cells[0].text
            record['Per'] = table_cells[1].text
            record['Time'] = table_cells[2].text
            record['Str'] = table_cells[3].text
            record['Team'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            n += 1
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save_var('record', record)
    #scraperwiki.sqlite.save_var(gid, save)
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
    url = "http://www.nhl.com/scores/htmlreports/20112012/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object

# scrape_table function: gets passed an individual page to scrape
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    n = 1
    for row in rows:
        # Set up our data record - we'll need it later 
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['gid'] = gid
            record['Goal'] = table_cells[0].text
            record['Per'] = table_cells[1].text
            record['Time'] = table_cells[2].text
            record['Str'] = table_cells[3].text
            record['Team'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            n += 1
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save_var('record', record)
    #scraperwiki.sqlite.save_var(gid, save)
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
    url = "http://www.nhl.com/scores/htmlreports/20112012/GS0" + str(gid) + ".HTM"
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object

# scrape_table function: gets passed an individual page to scrape
    tables = root.cssselect("#MainTable table")[8]
    rows = tables.cssselect("tr")  # selects all <tr> blocks within <table class="data">
    n = 1
    for row in rows:
        # Set up our data record - we'll need it later 
        record = {}
        table_cells = row.cssselect("td")
        if table_cells:
            record['gid'] = gid
            record['Goal'] = table_cells[0].text
            record['Per'] = table_cells[1].text
            record['Time'] = table_cells[2].text
            record['Str'] = table_cells[3].text
            record['Team'] = table_cells[4].text
            # Print out the data we've gathered
            print record, '------------'
            n += 1
            # Finally, save the record to the datastore - 'Artist' is our unique key
            scraperwiki.sqlite.save_var('record', record)
    #scraperwiki.sqlite.save_var(gid, save)
    time.sleep(3) # delay X seconds to throttle URL fetching


