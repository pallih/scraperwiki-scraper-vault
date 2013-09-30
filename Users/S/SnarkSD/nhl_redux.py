import scraperwiki
import lxml.etree
import lxml.html
import time

gameurlstart = "http://www.nhl.com/scores/htmlreports/20112012/PL02"
gameurlend = ".HTM"

gids = ["0002", "0011", "0049", "0064", "0079", "0080", "0098", "0110",
        "0127", "0142", "0154", "0166", "0171", "0184", "0203", "0216",
        "0230", "0248", "0265", "0277", "0286", "0297", "0324", "0340",
        "0353", "0373", "0387", "0392", "0417", "0438", "0462", "0467",
        "0482", "0500", "0510", "0533", "0544", "0562", "0575", "0585",
        "0603", "0617", "0644", "0649", "0670", "0685", "0702", "0716",
        "0723", "0739", "0750", "0771", "0783", "0794", "0804", "0822",
        "0845", "0849", "0870", "0886", "0899", "0918", "0938", "0947",
        "0966", "0984", "0997", "1016", "1025", "1041", "1056", "1069",
        "1082", "1088", "1110", "1119", "1141", "1155", "1171", "1190",
        "1201", "1222"]

oppids = ["MTL", "OTT", "CGY", "COL", "WPG", "BOS", "MTL", "PHI",
        "NYR", "PIT", "OTT", "N.J", "CBJ", "BOS", "FLA", "STL",
        "OTT", "PHX", "NSH", "WSH", "CAR", "T.B", "DAL", "ANA",
        "BOS", "BOS", "NYR", "N.J", "WSH", "CAR", "BUF", "VAN",
        "L.A", "BUF", "NYI", "FLA", "CAR", "WPG", "T.B", "WPG",
        "DET", "BUF", "BUF", "NYR", "OTT", "MIN", "MTL", "NYI",
        "NYI", "PIT", "PIT", "OTT", "EDM", "WPG", "PHI", "MTL",
        "CGY", "EDM", "VAN", "N.J", "S.J", "WSH", "FLA", "CHI",
        "MTL", "BOS", "PIT", "PHI", "WSH", "FLA", "T.B", "OTT",
        "BOS", "NYI", "N.J", "NYR", "CAR", "PHI", "BUF", "BUF",
        "T.B", "MTL"]

#game1url = gameurlstart + game1id + gameurlend
#html = scraperwiki.scrape(game1url)
#html = scraperwiki.scrape('http://www.nhl.com/scores/htmlreports/20112012/PL020002.HTM')

leafsgoals = oppgoals = leafsevcorsi = oppevcorsi = leafsfentied = oppfentied = leafsfenup2 = oppfenup2 = j = 0
for gid in gids:
    url = gameurlstart + str(gid) + gameurlend
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    
    awayteam = root.cssselect("#Visitor td")[5].text # assign the contents of the 5th <td> in the html element with id "Visitor" to awayteam
    hometeam = root.cssselect("#Home td")[5].text
    
    if hometeam == "TORONTO MAPLE LEAFS": # need to use a lookup table (if-statement) for weird team shortenings, e.g. Washington -> WSH
        hometeamshort = "TOR"
        awayteamshort = oppids[j]
    elif awayteam == "TORONTO MAPLE LEAFS":
        awayteamshort = "TOR"
        hometeamshort = oppids[j]
    else:
        print "Uh Oh!"
        break
    #awayteamshort = "MTL" # hardcoded for one specific game
    
    homegoals = awaygoals = homecorsi = awaycorsi = homeevcorsi = awayevcorsi = homeevcorsitied = awayevcorsitied = homeevfentied = awayevfentied = i = 0
    tds = root.cssselect("td") # assign all <td> elements to a list called "tds"
    
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if (td.text == "GOAL") and (tds[i - 3].text != "5"): # if the <td>'s contents are "Goal" and the period isn't the 5th (i.e. the shootout)
            if tds[i + 1].text.startswith(hometeamshort): # check if the next table cell starts with the same letters as the home team
                if (homegoals == awaygoals) and (tds[i - 2].text == "EV"): # check if the score is tied BEFORE the goal and if the play was at even strength
                    homeevcorsitied += 1 # if so, adjust the corsi-tied and fenwick-tied counts appropriately
                    homeevfentied += 1
                elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2):
                    leafsfenup2 += 1
                elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2):
                    oppfenup2 += 1
                if tds[i - 2].text == "EV":
                    homeevcorsi += 1
                homegoals += 1
                homecorsi += 1
            elif tds[i + 1].text.startswith(awayteamshort):
                if (homegoals == awaygoals) and (tds[i - 2].text == "EV"):
                    awayevcorsitied += 1
                    awayevfentied += 1
                elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2):
                    oppfenup2 += 1
                elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2):
                    leafsfenup2 += 1
                awaygoals +=1
                awaycorsi += 1
                if tds[i - 2].text == "EV":            
                    awayevcorsi += 1
        elif ((td.text == "SHOT") or (td.text == "MISS") or (td.text == "BLOCK")) and (tds[i - 3].text != "5"):
            if tds[i + 1].text.startswith(hometeamshort):
                homecorsi += 1
                if tds[i - 2].text == "EV":
                    homeevcorsi += 1
                    if homegoals == awaygoals:
                        homeevcorsitied += 1
                        if td.text != "BLOCK":
                            homeevfentied += 1
                    elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2) and (td.text != "BLOCK"):
                        leafsfenup2 += 1
                    elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2) and (td.text != "BLOCK"):
                        oppfenup2 += 1
            elif tds[i + 1].text.startswith(awayteamshort):
                awaycorsi += 1
                if tds[i - 2].text == "EV":
                    awayevcorsi += 1
                    if homegoals == awaygoals:
                        awayevcorsitied +=1
                        if td.text != "BLOCK":
                            awayevfentied += 1
                    elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2) and (td.text != "BLOCK"):
                        oppfenup2 += 1
                    elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2) and (td.text != "BLOCK"):
                        leafsfenup2 += 1
        i += 1
    
    print "Final score:", awayteam, " ", awaygoals, "at ", hometeam, " ", homegoals
    if awayevcorsitied + homeevcorsitied > 0:
        awayevcorsitiedpct = 100.0 * awayevcorsitied / (awayevcorsitied + homeevcorsitied)
        homeevcorsitiedpct = 100.0 * homeevcorsitied / (awayevcorsitied + homeevcorsitied)
    if awayevfentied + homeevfentied > 0:
        awayevfentiedpct = 100.0 * awayevfentied / (awayevfentied + homeevfentied)
        homeevfentiedpct = 100.0 * homeevfentied / (awayevfentied + homeevfentied)
    if hometeam == "TORONTO MAPLE LEAFS":
        leafsevcorsi += homeevcorsi
        oppevcorsi += awayevcorsi
        leafsfentied += homeevfentied
        oppfentied += awayevfentied
        leafsgoals += homegoals
        oppgoals += awaygoals
    elif awayteam == "TORONTO MAPLE LEAFS":
        leafsevcorsi += awayevcorsi
        oppevcorsi += homeevcorsi
        leafsfentied += awayevfentied
        oppfentied += homeevfentied
        leafsgoals += awaygoals
        oppgoals += homegoals
    leafsevcorsipct = 100.0 * leafsevcorsi / ( leafsevcorsi + oppevcorsi )
    leafsfentiedpct = 100.0 * leafsfentied / ( leafsfentied + oppfentied )
    leafsfenup2pct = 100.0 * leafsfenup2 / ( leafsfenup2 + oppfenup2 )
    #print "Corsi:", awayteam, " ", awaycorsi, "- ", hometeam, " ", homecorsi
    #print "EV Corsi running totals: Leafs", leafsevcorsi, "Opponents", oppevcorsi
    print "Leafs' EV Corsi % running total", leafsevcorsipct
    print "EV Corsi tied:", awayteam, " ", awayevcorsitied, "- ", hometeam, " ", homeevcorsitied
    #print "EV Corsi tied%:", awayteam, " ", awayevcorsitiedpct, "% - ", hometeam, " ", homeevcorsitiedpct, "%"
    #print "EV Fen tied:", awayteam, " ", awayevfentied, "- ", hometeam, " ", homeevfentied
    #print "EV Fen tied %:", awayteam, " ", awayevfentiedpct, "% - ", hometeam, " ", homeevfentiedpct, "%"
    #print "Leafs' EV Fen tied % running total: ", leafsfentiedpct
    #print "EV Fen up 2 running totals: Leafs", leafsfenup2, "Opponents", oppfenup2
    #print "EV Fen up 2 % running total: Leafs", leafsfenup2pct
    #print "Running total: Leafs' goals for: ", leafsgoals, "; goals against: ", oppgoals 
    j += 1
    time.sleep(4) # delay X seconds to throttle URL fetching

print "Leafs' EV Fen tied: ", leafsfentied
print "Opponents' EV Fen tied: ", oppfentied
print "Leafs' EV Corsi: ", leafsevcorsipct
print "Leafs' EV Fen tied %: ", leafsfentiedpct # 46.99 here (47.07 including shootouts, 46.93 excluding OT and SO); 46.48 from BTN
print "Leafs' EV Fen up 2 %: ", leafsfenup2pct
print "Leafs' goals for: ", leafsgoals, "; goals against: ", oppgoals # 227/259 here AND from NHL.com

#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.sqlite.save(["td"], record) # save the records one by one
# Blank Python

import scraperwiki
import lxml.etree
import lxml.html
import time

gameurlstart = "http://www.nhl.com/scores/htmlreports/20112012/PL02"
gameurlend = ".HTM"

gids = ["0002", "0011", "0049", "0064", "0079", "0080", "0098", "0110",
        "0127", "0142", "0154", "0166", "0171", "0184", "0203", "0216",
        "0230", "0248", "0265", "0277", "0286", "0297", "0324", "0340",
        "0353", "0373", "0387", "0392", "0417", "0438", "0462", "0467",
        "0482", "0500", "0510", "0533", "0544", "0562", "0575", "0585",
        "0603", "0617", "0644", "0649", "0670", "0685", "0702", "0716",
        "0723", "0739", "0750", "0771", "0783", "0794", "0804", "0822",
        "0845", "0849", "0870", "0886", "0899", "0918", "0938", "0947",
        "0966", "0984", "0997", "1016", "1025", "1041", "1056", "1069",
        "1082", "1088", "1110", "1119", "1141", "1155", "1171", "1190",
        "1201", "1222"]

oppids = ["MTL", "OTT", "CGY", "COL", "WPG", "BOS", "MTL", "PHI",
        "NYR", "PIT", "OTT", "N.J", "CBJ", "BOS", "FLA", "STL",
        "OTT", "PHX", "NSH", "WSH", "CAR", "T.B", "DAL", "ANA",
        "BOS", "BOS", "NYR", "N.J", "WSH", "CAR", "BUF", "VAN",
        "L.A", "BUF", "NYI", "FLA", "CAR", "WPG", "T.B", "WPG",
        "DET", "BUF", "BUF", "NYR", "OTT", "MIN", "MTL", "NYI",
        "NYI", "PIT", "PIT", "OTT", "EDM", "WPG", "PHI", "MTL",
        "CGY", "EDM", "VAN", "N.J", "S.J", "WSH", "FLA", "CHI",
        "MTL", "BOS", "PIT", "PHI", "WSH", "FLA", "T.B", "OTT",
        "BOS", "NYI", "N.J", "NYR", "CAR", "PHI", "BUF", "BUF",
        "T.B", "MTL"]

#game1url = gameurlstart + game1id + gameurlend
#html = scraperwiki.scrape(game1url)
#html = scraperwiki.scrape('http://www.nhl.com/scores/htmlreports/20112012/PL020002.HTM')

leafsgoals = oppgoals = leafsevcorsi = oppevcorsi = leafsfentied = oppfentied = leafsfenup2 = oppfenup2 = j = 0
for gid in gids:
    url = gameurlstart + str(gid) + gameurlend
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    
    awayteam = root.cssselect("#Visitor td")[5].text # assign the contents of the 5th <td> in the html element with id "Visitor" to awayteam
    hometeam = root.cssselect("#Home td")[5].text
    
    if hometeam == "TORONTO MAPLE LEAFS": # need to use a lookup table (if-statement) for weird team shortenings, e.g. Washington -> WSH
        hometeamshort = "TOR"
        awayteamshort = oppids[j]
    elif awayteam == "TORONTO MAPLE LEAFS":
        awayteamshort = "TOR"
        hometeamshort = oppids[j]
    else:
        print "Uh Oh!"
        break
    #awayteamshort = "MTL" # hardcoded for one specific game
    
    homegoals = awaygoals = homecorsi = awaycorsi = homeevcorsi = awayevcorsi = homeevcorsitied = awayevcorsitied = homeevfentied = awayevfentied = i = 0
    tds = root.cssselect("td") # assign all <td> elements to a list called "tds"
    
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if (td.text == "GOAL") and (tds[i - 3].text != "5"): # if the <td>'s contents are "Goal" and the period isn't the 5th (i.e. the shootout)
            if tds[i + 1].text.startswith(hometeamshort): # check if the next table cell starts with the same letters as the home team
                if (homegoals == awaygoals) and (tds[i - 2].text == "EV"): # check if the score is tied BEFORE the goal and if the play was at even strength
                    homeevcorsitied += 1 # if so, adjust the corsi-tied and fenwick-tied counts appropriately
                    homeevfentied += 1
                elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2):
                    leafsfenup2 += 1
                elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2):
                    oppfenup2 += 1
                if tds[i - 2].text == "EV":
                    homeevcorsi += 1
                homegoals += 1
                homecorsi += 1
            elif tds[i + 1].text.startswith(awayteamshort):
                if (homegoals == awaygoals) and (tds[i - 2].text == "EV"):
                    awayevcorsitied += 1
                    awayevfentied += 1
                elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2):
                    oppfenup2 += 1
                elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2):
                    leafsfenup2 += 1
                awaygoals +=1
                awaycorsi += 1
                if tds[i - 2].text == "EV":            
                    awayevcorsi += 1
        elif ((td.text == "SHOT") or (td.text == "MISS") or (td.text == "BLOCK")) and (tds[i - 3].text != "5"):
            if tds[i + 1].text.startswith(hometeamshort):
                homecorsi += 1
                if tds[i - 2].text == "EV":
                    homeevcorsi += 1
                    if homegoals == awaygoals:
                        homeevcorsitied += 1
                        if td.text != "BLOCK":
                            homeevfentied += 1
                    elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2) and (td.text != "BLOCK"):
                        leafsfenup2 += 1
                    elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2) and (td.text != "BLOCK"):
                        oppfenup2 += 1
            elif tds[i + 1].text.startswith(awayteamshort):
                awaycorsi += 1
                if tds[i - 2].text == "EV":
                    awayevcorsi += 1
                    if homegoals == awaygoals:
                        awayevcorsitied +=1
                        if td.text != "BLOCK":
                            awayevfentied += 1
                    elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2) and (td.text != "BLOCK"):
                        oppfenup2 += 1
                    elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2) and (td.text != "BLOCK"):
                        leafsfenup2 += 1
        i += 1
    
    print "Final score:", awayteam, " ", awaygoals, "at ", hometeam, " ", homegoals
    if awayevcorsitied + homeevcorsitied > 0:
        awayevcorsitiedpct = 100.0 * awayevcorsitied / (awayevcorsitied + homeevcorsitied)
        homeevcorsitiedpct = 100.0 * homeevcorsitied / (awayevcorsitied + homeevcorsitied)
    if awayevfentied + homeevfentied > 0:
        awayevfentiedpct = 100.0 * awayevfentied / (awayevfentied + homeevfentied)
        homeevfentiedpct = 100.0 * homeevfentied / (awayevfentied + homeevfentied)
    if hometeam == "TORONTO MAPLE LEAFS":
        leafsevcorsi += homeevcorsi
        oppevcorsi += awayevcorsi
        leafsfentied += homeevfentied
        oppfentied += awayevfentied
        leafsgoals += homegoals
        oppgoals += awaygoals
    elif awayteam == "TORONTO MAPLE LEAFS":
        leafsevcorsi += awayevcorsi
        oppevcorsi += homeevcorsi
        leafsfentied += awayevfentied
        oppfentied += homeevfentied
        leafsgoals += awaygoals
        oppgoals += homegoals
    leafsevcorsipct = 100.0 * leafsevcorsi / ( leafsevcorsi + oppevcorsi )
    leafsfentiedpct = 100.0 * leafsfentied / ( leafsfentied + oppfentied )
    leafsfenup2pct = 100.0 * leafsfenup2 / ( leafsfenup2 + oppfenup2 )
    #print "Corsi:", awayteam, " ", awaycorsi, "- ", hometeam, " ", homecorsi
    #print "EV Corsi running totals: Leafs", leafsevcorsi, "Opponents", oppevcorsi
    print "Leafs' EV Corsi % running total", leafsevcorsipct
    print "EV Corsi tied:", awayteam, " ", awayevcorsitied, "- ", hometeam, " ", homeevcorsitied
    #print "EV Corsi tied%:", awayteam, " ", awayevcorsitiedpct, "% - ", hometeam, " ", homeevcorsitiedpct, "%"
    #print "EV Fen tied:", awayteam, " ", awayevfentied, "- ", hometeam, " ", homeevfentied
    #print "EV Fen tied %:", awayteam, " ", awayevfentiedpct, "% - ", hometeam, " ", homeevfentiedpct, "%"
    #print "Leafs' EV Fen tied % running total: ", leafsfentiedpct
    #print "EV Fen up 2 running totals: Leafs", leafsfenup2, "Opponents", oppfenup2
    #print "EV Fen up 2 % running total: Leafs", leafsfenup2pct
    #print "Running total: Leafs' goals for: ", leafsgoals, "; goals against: ", oppgoals 
    j += 1
    time.sleep(4) # delay X seconds to throttle URL fetching

print "Leafs' EV Fen tied: ", leafsfentied
print "Opponents' EV Fen tied: ", oppfentied
print "Leafs' EV Corsi: ", leafsevcorsipct
print "Leafs' EV Fen tied %: ", leafsfentiedpct # 46.99 here (47.07 including shootouts, 46.93 excluding OT and SO); 46.48 from BTN
print "Leafs' EV Fen up 2 %: ", leafsfenup2pct
print "Leafs' goals for: ", leafsgoals, "; goals against: ", oppgoals # 227/259 here AND from NHL.com

#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.sqlite.save(["td"], record) # save the records one by one
# Blank Python

import scraperwiki
import lxml.etree
import lxml.html
import time

gameurlstart = "http://www.nhl.com/scores/htmlreports/20112012/PL02"
gameurlend = ".HTM"

gids = ["0002", "0011", "0049", "0064", "0079", "0080", "0098", "0110",
        "0127", "0142", "0154", "0166", "0171", "0184", "0203", "0216",
        "0230", "0248", "0265", "0277", "0286", "0297", "0324", "0340",
        "0353", "0373", "0387", "0392", "0417", "0438", "0462", "0467",
        "0482", "0500", "0510", "0533", "0544", "0562", "0575", "0585",
        "0603", "0617", "0644", "0649", "0670", "0685", "0702", "0716",
        "0723", "0739", "0750", "0771", "0783", "0794", "0804", "0822",
        "0845", "0849", "0870", "0886", "0899", "0918", "0938", "0947",
        "0966", "0984", "0997", "1016", "1025", "1041", "1056", "1069",
        "1082", "1088", "1110", "1119", "1141", "1155", "1171", "1190",
        "1201", "1222"]

oppids = ["MTL", "OTT", "CGY", "COL", "WPG", "BOS", "MTL", "PHI",
        "NYR", "PIT", "OTT", "N.J", "CBJ", "BOS", "FLA", "STL",
        "OTT", "PHX", "NSH", "WSH", "CAR", "T.B", "DAL", "ANA",
        "BOS", "BOS", "NYR", "N.J", "WSH", "CAR", "BUF", "VAN",
        "L.A", "BUF", "NYI", "FLA", "CAR", "WPG", "T.B", "WPG",
        "DET", "BUF", "BUF", "NYR", "OTT", "MIN", "MTL", "NYI",
        "NYI", "PIT", "PIT", "OTT", "EDM", "WPG", "PHI", "MTL",
        "CGY", "EDM", "VAN", "N.J", "S.J", "WSH", "FLA", "CHI",
        "MTL", "BOS", "PIT", "PHI", "WSH", "FLA", "T.B", "OTT",
        "BOS", "NYI", "N.J", "NYR", "CAR", "PHI", "BUF", "BUF",
        "T.B", "MTL"]

#game1url = gameurlstart + game1id + gameurlend
#html = scraperwiki.scrape(game1url)
#html = scraperwiki.scrape('http://www.nhl.com/scores/htmlreports/20112012/PL020002.HTM')

leafsgoals = oppgoals = leafsevcorsi = oppevcorsi = leafsfentied = oppfentied = leafsfenup2 = oppfenup2 = j = 0
for gid in gids:
    url = gameurlstart + str(gid) + gameurlend
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    
    awayteam = root.cssselect("#Visitor td")[5].text # assign the contents of the 5th <td> in the html element with id "Visitor" to awayteam
    hometeam = root.cssselect("#Home td")[5].text
    
    if hometeam == "TORONTO MAPLE LEAFS": # need to use a lookup table (if-statement) for weird team shortenings, e.g. Washington -> WSH
        hometeamshort = "TOR"
        awayteamshort = oppids[j]
    elif awayteam == "TORONTO MAPLE LEAFS":
        awayteamshort = "TOR"
        hometeamshort = oppids[j]
    else:
        print "Uh Oh!"
        break
    #awayteamshort = "MTL" # hardcoded for one specific game
    
    homegoals = awaygoals = homecorsi = awaycorsi = homeevcorsi = awayevcorsi = homeevcorsitied = awayevcorsitied = homeevfentied = awayevfentied = i = 0
    tds = root.cssselect("td") # assign all <td> elements to a list called "tds"
    
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if (td.text == "GOAL") and (tds[i - 3].text != "5"): # if the <td>'s contents are "Goal" and the period isn't the 5th (i.e. the shootout)
            if tds[i + 1].text.startswith(hometeamshort): # check if the next table cell starts with the same letters as the home team
                if (homegoals == awaygoals) and (tds[i - 2].text == "EV"): # check if the score is tied BEFORE the goal and if the play was at even strength
                    homeevcorsitied += 1 # if so, adjust the corsi-tied and fenwick-tied counts appropriately
                    homeevfentied += 1
                elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2):
                    leafsfenup2 += 1
                elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2):
                    oppfenup2 += 1
                if tds[i - 2].text == "EV":
                    homeevcorsi += 1
                homegoals += 1
                homecorsi += 1
            elif tds[i + 1].text.startswith(awayteamshort):
                if (homegoals == awaygoals) and (tds[i - 2].text == "EV"):
                    awayevcorsitied += 1
                    awayevfentied += 1
                elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2):
                    oppfenup2 += 1
                elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2):
                    leafsfenup2 += 1
                awaygoals +=1
                awaycorsi += 1
                if tds[i - 2].text == "EV":            
                    awayevcorsi += 1
        elif ((td.text == "SHOT") or (td.text == "MISS") or (td.text == "BLOCK")) and (tds[i - 3].text != "5"):
            if tds[i + 1].text.startswith(hometeamshort):
                homecorsi += 1
                if tds[i - 2].text == "EV":
                    homeevcorsi += 1
                    if homegoals == awaygoals:
                        homeevcorsitied += 1
                        if td.text != "BLOCK":
                            homeevfentied += 1
                    elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2) and (td.text != "BLOCK"):
                        leafsfenup2 += 1
                    elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2) and (td.text != "BLOCK"):
                        oppfenup2 += 1
            elif tds[i + 1].text.startswith(awayteamshort):
                awaycorsi += 1
                if tds[i - 2].text == "EV":
                    awayevcorsi += 1
                    if homegoals == awaygoals:
                        awayevcorsitied +=1
                        if td.text != "BLOCK":
                            awayevfentied += 1
                    elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2) and (td.text != "BLOCK"):
                        oppfenup2 += 1
                    elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2) and (td.text != "BLOCK"):
                        leafsfenup2 += 1
        i += 1
    
    print "Final score:", awayteam, " ", awaygoals, "at ", hometeam, " ", homegoals
    if awayevcorsitied + homeevcorsitied > 0:
        awayevcorsitiedpct = 100.0 * awayevcorsitied / (awayevcorsitied + homeevcorsitied)
        homeevcorsitiedpct = 100.0 * homeevcorsitied / (awayevcorsitied + homeevcorsitied)
    if awayevfentied + homeevfentied > 0:
        awayevfentiedpct = 100.0 * awayevfentied / (awayevfentied + homeevfentied)
        homeevfentiedpct = 100.0 * homeevfentied / (awayevfentied + homeevfentied)
    if hometeam == "TORONTO MAPLE LEAFS":
        leafsevcorsi += homeevcorsi
        oppevcorsi += awayevcorsi
        leafsfentied += homeevfentied
        oppfentied += awayevfentied
        leafsgoals += homegoals
        oppgoals += awaygoals
    elif awayteam == "TORONTO MAPLE LEAFS":
        leafsevcorsi += awayevcorsi
        oppevcorsi += homeevcorsi
        leafsfentied += awayevfentied
        oppfentied += homeevfentied
        leafsgoals += awaygoals
        oppgoals += homegoals
    leafsevcorsipct = 100.0 * leafsevcorsi / ( leafsevcorsi + oppevcorsi )
    leafsfentiedpct = 100.0 * leafsfentied / ( leafsfentied + oppfentied )
    leafsfenup2pct = 100.0 * leafsfenup2 / ( leafsfenup2 + oppfenup2 )
    #print "Corsi:", awayteam, " ", awaycorsi, "- ", hometeam, " ", homecorsi
    #print "EV Corsi running totals: Leafs", leafsevcorsi, "Opponents", oppevcorsi
    print "Leafs' EV Corsi % running total", leafsevcorsipct
    print "EV Corsi tied:", awayteam, " ", awayevcorsitied, "- ", hometeam, " ", homeevcorsitied
    #print "EV Corsi tied%:", awayteam, " ", awayevcorsitiedpct, "% - ", hometeam, " ", homeevcorsitiedpct, "%"
    #print "EV Fen tied:", awayteam, " ", awayevfentied, "- ", hometeam, " ", homeevfentied
    #print "EV Fen tied %:", awayteam, " ", awayevfentiedpct, "% - ", hometeam, " ", homeevfentiedpct, "%"
    #print "Leafs' EV Fen tied % running total: ", leafsfentiedpct
    #print "EV Fen up 2 running totals: Leafs", leafsfenup2, "Opponents", oppfenup2
    #print "EV Fen up 2 % running total: Leafs", leafsfenup2pct
    #print "Running total: Leafs' goals for: ", leafsgoals, "; goals against: ", oppgoals 
    j += 1
    time.sleep(4) # delay X seconds to throttle URL fetching

print "Leafs' EV Fen tied: ", leafsfentied
print "Opponents' EV Fen tied: ", oppfentied
print "Leafs' EV Corsi: ", leafsevcorsipct
print "Leafs' EV Fen tied %: ", leafsfentiedpct # 46.99 here (47.07 including shootouts, 46.93 excluding OT and SO); 46.48 from BTN
print "Leafs' EV Fen up 2 %: ", leafsfenup2pct
print "Leafs' goals for: ", leafsgoals, "; goals against: ", oppgoals # 227/259 here AND from NHL.com

#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.sqlite.save(["td"], record) # save the records one by one
# Blank Python

import scraperwiki
import lxml.etree
import lxml.html
import time

gameurlstart = "http://www.nhl.com/scores/htmlreports/20112012/PL02"
gameurlend = ".HTM"

gids = ["0002", "0011", "0049", "0064", "0079", "0080", "0098", "0110",
        "0127", "0142", "0154", "0166", "0171", "0184", "0203", "0216",
        "0230", "0248", "0265", "0277", "0286", "0297", "0324", "0340",
        "0353", "0373", "0387", "0392", "0417", "0438", "0462", "0467",
        "0482", "0500", "0510", "0533", "0544", "0562", "0575", "0585",
        "0603", "0617", "0644", "0649", "0670", "0685", "0702", "0716",
        "0723", "0739", "0750", "0771", "0783", "0794", "0804", "0822",
        "0845", "0849", "0870", "0886", "0899", "0918", "0938", "0947",
        "0966", "0984", "0997", "1016", "1025", "1041", "1056", "1069",
        "1082", "1088", "1110", "1119", "1141", "1155", "1171", "1190",
        "1201", "1222"]

oppids = ["MTL", "OTT", "CGY", "COL", "WPG", "BOS", "MTL", "PHI",
        "NYR", "PIT", "OTT", "N.J", "CBJ", "BOS", "FLA", "STL",
        "OTT", "PHX", "NSH", "WSH", "CAR", "T.B", "DAL", "ANA",
        "BOS", "BOS", "NYR", "N.J", "WSH", "CAR", "BUF", "VAN",
        "L.A", "BUF", "NYI", "FLA", "CAR", "WPG", "T.B", "WPG",
        "DET", "BUF", "BUF", "NYR", "OTT", "MIN", "MTL", "NYI",
        "NYI", "PIT", "PIT", "OTT", "EDM", "WPG", "PHI", "MTL",
        "CGY", "EDM", "VAN", "N.J", "S.J", "WSH", "FLA", "CHI",
        "MTL", "BOS", "PIT", "PHI", "WSH", "FLA", "T.B", "OTT",
        "BOS", "NYI", "N.J", "NYR", "CAR", "PHI", "BUF", "BUF",
        "T.B", "MTL"]

#game1url = gameurlstart + game1id + gameurlend
#html = scraperwiki.scrape(game1url)
#html = scraperwiki.scrape('http://www.nhl.com/scores/htmlreports/20112012/PL020002.HTM')

leafsgoals = oppgoals = leafsevcorsi = oppevcorsi = leafsfentied = oppfentied = leafsfenup2 = oppfenup2 = j = 0
for gid in gids:
    url = gameurlstart + str(gid) + gameurlend
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html) # turn HTML into an lxml object
    
    awayteam = root.cssselect("#Visitor td")[5].text # assign the contents of the 5th <td> in the html element with id "Visitor" to awayteam
    hometeam = root.cssselect("#Home td")[5].text
    
    if hometeam == "TORONTO MAPLE LEAFS": # need to use a lookup table (if-statement) for weird team shortenings, e.g. Washington -> WSH
        hometeamshort = "TOR"
        awayteamshort = oppids[j]
    elif awayteam == "TORONTO MAPLE LEAFS":
        awayteamshort = "TOR"
        hometeamshort = oppids[j]
    else:
        print "Uh Oh!"
        break
    #awayteamshort = "MTL" # hardcoded for one specific game
    
    homegoals = awaygoals = homecorsi = awaycorsi = homeevcorsi = awayevcorsi = homeevcorsitied = awayevcorsitied = homeevfentied = awayevfentied = i = 0
    tds = root.cssselect("td") # assign all <td> elements to a list called "tds"
    
    for td in tds: # iterate over each of the <td> elements (i.e. elements of the list called "tds")
        if (td.text == "GOAL") and (tds[i - 3].text != "5"): # if the <td>'s contents are "Goal" and the period isn't the 5th (i.e. the shootout)
            if tds[i + 1].text.startswith(hometeamshort): # check if the next table cell starts with the same letters as the home team
                if (homegoals == awaygoals) and (tds[i - 2].text == "EV"): # check if the score is tied BEFORE the goal and if the play was at even strength
                    homeevcorsitied += 1 # if so, adjust the corsi-tied and fenwick-tied counts appropriately
                    homeevfentied += 1
                elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2):
                    leafsfenup2 += 1
                elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2):
                    oppfenup2 += 1
                if tds[i - 2].text == "EV":
                    homeevcorsi += 1
                homegoals += 1
                homecorsi += 1
            elif tds[i + 1].text.startswith(awayteamshort):
                if (homegoals == awaygoals) and (tds[i - 2].text == "EV"):
                    awayevcorsitied += 1
                    awayevfentied += 1
                elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2):
                    oppfenup2 += 1
                elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2):
                    leafsfenup2 += 1
                awaygoals +=1
                awaycorsi += 1
                if tds[i - 2].text == "EV":            
                    awayevcorsi += 1
        elif ((td.text == "SHOT") or (td.text == "MISS") or (td.text == "BLOCK")) and (tds[i - 3].text != "5"):
            if tds[i + 1].text.startswith(hometeamshort):
                homecorsi += 1
                if tds[i - 2].text == "EV":
                    homeevcorsi += 1
                    if homegoals == awaygoals:
                        homeevcorsitied += 1
                        if td.text != "BLOCK":
                            homeevfentied += 1
                    elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2) and (td.text != "BLOCK"):
                        leafsfenup2 += 1
                    elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2) and (td.text != "BLOCK"):
                        oppfenup2 += 1
            elif tds[i + 1].text.startswith(awayteamshort):
                awaycorsi += 1
                if tds[i - 2].text == "EV":
                    awayevcorsi += 1
                    if homegoals == awaygoals:
                        awayevcorsitied +=1
                        if td.text != "BLOCK":
                            awayevfentied += 1
                    elif (hometeamshort == "TOR") and (homegoals == awaygoals + 2) and (td.text != "BLOCK"):
                        oppfenup2 += 1
                    elif (awayteamshort == "TOR") and (awaygoals == homegoals + 2) and (td.text != "BLOCK"):
                        leafsfenup2 += 1
        i += 1
    
    print "Final score:", awayteam, " ", awaygoals, "at ", hometeam, " ", homegoals
    if awayevcorsitied + homeevcorsitied > 0:
        awayevcorsitiedpct = 100.0 * awayevcorsitied / (awayevcorsitied + homeevcorsitied)
        homeevcorsitiedpct = 100.0 * homeevcorsitied / (awayevcorsitied + homeevcorsitied)
    if awayevfentied + homeevfentied > 0:
        awayevfentiedpct = 100.0 * awayevfentied / (awayevfentied + homeevfentied)
        homeevfentiedpct = 100.0 * homeevfentied / (awayevfentied + homeevfentied)
    if hometeam == "TORONTO MAPLE LEAFS":
        leafsevcorsi += homeevcorsi
        oppevcorsi += awayevcorsi
        leafsfentied += homeevfentied
        oppfentied += awayevfentied
        leafsgoals += homegoals
        oppgoals += awaygoals
    elif awayteam == "TORONTO MAPLE LEAFS":
        leafsevcorsi += awayevcorsi
        oppevcorsi += homeevcorsi
        leafsfentied += awayevfentied
        oppfentied += homeevfentied
        leafsgoals += awaygoals
        oppgoals += homegoals
    leafsevcorsipct = 100.0 * leafsevcorsi / ( leafsevcorsi + oppevcorsi )
    leafsfentiedpct = 100.0 * leafsfentied / ( leafsfentied + oppfentied )
    leafsfenup2pct = 100.0 * leafsfenup2 / ( leafsfenup2 + oppfenup2 )
    #print "Corsi:", awayteam, " ", awaycorsi, "- ", hometeam, " ", homecorsi
    #print "EV Corsi running totals: Leafs", leafsevcorsi, "Opponents", oppevcorsi
    print "Leafs' EV Corsi % running total", leafsevcorsipct
    print "EV Corsi tied:", awayteam, " ", awayevcorsitied, "- ", hometeam, " ", homeevcorsitied
    #print "EV Corsi tied%:", awayteam, " ", awayevcorsitiedpct, "% - ", hometeam, " ", homeevcorsitiedpct, "%"
    #print "EV Fen tied:", awayteam, " ", awayevfentied, "- ", hometeam, " ", homeevfentied
    #print "EV Fen tied %:", awayteam, " ", awayevfentiedpct, "% - ", hometeam, " ", homeevfentiedpct, "%"
    #print "Leafs' EV Fen tied % running total: ", leafsfentiedpct
    #print "EV Fen up 2 running totals: Leafs", leafsfenup2, "Opponents", oppfenup2
    #print "EV Fen up 2 % running total: Leafs", leafsfenup2pct
    #print "Running total: Leafs' goals for: ", leafsgoals, "; goals against: ", oppgoals 
    j += 1
    time.sleep(4) # delay X seconds to throttle URL fetching

print "Leafs' EV Fen tied: ", leafsfentied
print "Opponents' EV Fen tied: ", oppfentied
print "Leafs' EV Corsi: ", leafsevcorsipct
print "Leafs' EV Fen tied %: ", leafsfentiedpct # 46.99 here (47.07 including shootouts, 46.93 excluding OT and SO); 46.48 from BTN
print "Leafs' EV Fen up 2 %: ", leafsfenup2pct
print "Leafs' goals for: ", leafsgoals, "; goals against: ", oppgoals # 227/259 here AND from NHL.com

#for td in tds:
#     record = { "td" : td.text } # column name and value
#     scraperwiki.sqlite.save(["td"], record) # save the records one by one
# Blank Python

