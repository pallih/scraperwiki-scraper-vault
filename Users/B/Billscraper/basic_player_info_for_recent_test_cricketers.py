###############################################################################
# Gets basic info about recent test playing cricketers
###############################################################################

import scraperwiki
import lxml.html

def build_plyr_list(maxcountryno):
    playerlist = []
    #loop through different country pages 1-9 are test-playing nations, the rest are a bit random
    for countryno in range(1,maxcountryno):

        countryurl= "http://www.espncricinfo.com/ci/content/player/index.html?country="+str(countryno)
        html = scraperwiki.scrape(countryurl)
        root = lxml.html.fromstring(html)


        #currently only looks at 'recent' test players (i.e. on front page for each country)
        #historical data would be interesting but potentially many 000s of records
        for tr in root.cssselect("div#rectPlyr_Playerlistall table tr"):
            hrefs = tr.cssselect("a")
            #print hrefs

            if len(hrefs) >0:
                #extract each column in turn
                for col in range(0,3):
                    playerlist.append(hrefs[col].get('href'))
    print playerlist
    return playerlist

    # Loop through each player's page
    # dictionary to store info for each player
playerinfo = {'PlayerURL' : "", 'Full name' : "",'Playing role' : "",'Batting style' : "",'Bowling style' : ""}

for player in build_plyr_list(10):
    playerurl = "http://www.espncricinfo.com/" + player
    #print playerurl
    html2 = scraperwiki.scrape(playerurl)
    root2 = lxml.html.fromstring(html2)

    playerinfo['PlayerURL'] = playerurl

    #on each player page, loop through fields
    for el in root2.cssselect("p.ciPlayerinformationtxt"):
    #print "player loop"
        elb = el.cssselect("b")
        elsp = el.cssselect("span")

        fieldhdr = elb[0].text_content()
        fieldval = elsp[0].text_content()

        #print fieldhdr
        #print fieldval

        #if some players are missing certain fields, this will avoid errors or inconsistencies

        if fieldhdr == 'Full name':
            playerinfo[fieldhdr] = fieldval

        if fieldhdr == 'Playing role':
            playerinfo[fieldhdr] = fieldval

        if fieldhdr == 'Batting style':
            playerinfo[fieldhdr] = fieldval

        if fieldhdr == 'Bowling style':
            playerinfo[fieldhdr] = fieldval

        #PLAYER'S COUNTRY WOULD BE USEFUL TOO...


        #Other fields available:
        #Born    - could be interesting to look at ages/eras, but needs stripping down
        #Current age    -accurate at point of extraction
        #Height        -could be interesting (e.g. comparing bowlers to batsmen) but some metric, some imperial
        #Education    -type of school would be interesting, but matching to ext db may be tricky

    # Save player's data to db
    #print playerinfo
    scraperwiki.sqlite.save(unique_keys=['PlayerURL'], data=playerinfo)

###############################################################################
# Gets basic info about recent test playing cricketers
###############################################################################

import scraperwiki
import lxml.html

def build_plyr_list(maxcountryno):
    playerlist = []
    #loop through different country pages 1-9 are test-playing nations, the rest are a bit random
    for countryno in range(1,maxcountryno):

        countryurl= "http://www.espncricinfo.com/ci/content/player/index.html?country="+str(countryno)
        html = scraperwiki.scrape(countryurl)
        root = lxml.html.fromstring(html)


        #currently only looks at 'recent' test players (i.e. on front page for each country)
        #historical data would be interesting but potentially many 000s of records
        for tr in root.cssselect("div#rectPlyr_Playerlistall table tr"):
            hrefs = tr.cssselect("a")
            #print hrefs

            if len(hrefs) >0:
                #extract each column in turn
                for col in range(0,3):
                    playerlist.append(hrefs[col].get('href'))
    print playerlist
    return playerlist

    # Loop through each player's page
    # dictionary to store info for each player
playerinfo = {'PlayerURL' : "", 'Full name' : "",'Playing role' : "",'Batting style' : "",'Bowling style' : ""}

for player in build_plyr_list(10):
    playerurl = "http://www.espncricinfo.com/" + player
    #print playerurl
    html2 = scraperwiki.scrape(playerurl)
    root2 = lxml.html.fromstring(html2)

    playerinfo['PlayerURL'] = playerurl

    #on each player page, loop through fields
    for el in root2.cssselect("p.ciPlayerinformationtxt"):
    #print "player loop"
        elb = el.cssselect("b")
        elsp = el.cssselect("span")

        fieldhdr = elb[0].text_content()
        fieldval = elsp[0].text_content()

        #print fieldhdr
        #print fieldval

        #if some players are missing certain fields, this will avoid errors or inconsistencies

        if fieldhdr == 'Full name':
            playerinfo[fieldhdr] = fieldval

        if fieldhdr == 'Playing role':
            playerinfo[fieldhdr] = fieldval

        if fieldhdr == 'Batting style':
            playerinfo[fieldhdr] = fieldval

        if fieldhdr == 'Bowling style':
            playerinfo[fieldhdr] = fieldval

        #PLAYER'S COUNTRY WOULD BE USEFUL TOO...


        #Other fields available:
        #Born    - could be interesting to look at ages/eras, but needs stripping down
        #Current age    -accurate at point of extraction
        #Height        -could be interesting (e.g. comparing bowlers to batsmen) but some metric, some imperial
        #Education    -type of school would be interesting, but matching to ext db may be tricky

    # Save player's data to db
    #print playerinfo
    scraperwiki.sqlite.save(unique_keys=['PlayerURL'], data=playerinfo)

