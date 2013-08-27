#!/usr/bin/python

import scraperwiki
import lxml.html
import re
import urllib2

year = "2012"
siteURL = "http://dreamteam.afl.com.au"

rounds = ["/?p=topplayers"]
#rounds = [
#"/?p=topplayers&stats=round&round=1", "/?p=topplayers&stats=round&round=2", "/?p=topplayers&stats=round&round=3",
#"/?p=topplayers&stats=round&round=4", "/?p=topplayers&stats=round&round=5"
#"/?p=topplayers&stats=round&round=6", "/?p=topplayers&stats=round&round=7"
#"/?p=topplayers&stats=round&round=8""/?p=topplayers&stats=round&round=9"
#]

''' Gets links from the given round pages and scrapes them'''
def processRounds(roundURLs):
    for roundURL in roundURLs:
        html = urllib2.urlopen(siteURL + roundURL)
        roundPage = lxml.html.fromstring(html.read())
        html.close()
        
        round = roundPage.cssselect("li[id='tpRound'] a")[0].text_content().replace("round ", "").replace(" Rankings", "").strip()
        print "Round: " + round
        
        roundRows = roundPage.cssselect("div[id='view_standard'] tr")
        # specified in the footer
        pageLinks = roundRows[-1].cssselect("a")
        
        #remove the "next page" link
        del pageLinks[-1]
        
        for link in pageLinks:
            linkURL = siteURL + link.get("href")
            print linkURL
        
            scrapePage(linkURL, round)

        calculateExtraStats(round)

'''Scrapes an individual page'''
def scrapePage(pageURL, round):
    page = lxml.html.fromstring(scraperwiki.scrape(pageURL))
    rows = page.cssselect("div[id='view_standard'] tr")
    
    # remove footer and header row elements
    del rows[0]
    del rows[-1]
    del rows[-1]
    
    for tr in rows:
        tds = tr.cssselect("td")
        ths = tr.cssselect("th")

        # determine data
        playerURL = tds[1].cssselect("a[class='player-name']")[0].get("href")

        #player page info
        playerPage = lxml.html.fromstring(scraperwiki.scrape(siteURL + playerURL))
        roundRows = playerPage.cssselect("table[class='data'] tr")
        extraStats =  playerPage.cssselect("div[class='box']")
        
        roundIndex = int(-1)

        for i, roundRow in enumerate(roundRows):
            rowColumn = roundRow.cssselect("td[class='t1Head2 centered']")

            if (len(rowColumn) != 0 and rowColumn[0].text_content().strip() == round):
                roundIndex = i

        thisRound = roundRows[int(roundIndex)]

        # Variables
        name = tds[1].cssselect("a[class='player-name']")[0].text_content()
        pointsTotal = int(tds[8].text_content().replace(',', ''))

        data = {
          'year' : int(year),
          'round' : int(round),
          'player_id' : int(playerURL.replace('/player/','')),
          'name' : name,
          'price' : int(tds[1].cssselect("strong")[0].text_content().replace('$','').replace(',', '')),
          'games_played' : int(tds[2].text_content()),
          'num_selections' : int(tds[3].text_content().replace(',','')),
          'rank_last_round' : int(re.sub(' \(.+\)','', tds[4].text_content())),
          'mvp_value' : int(tds[5].text_content().replace(',','') if tds[5].text_content() != "N/A" else "0"),
          'points_last_round' : int(tds[7].text_content()),
          'points_avg' : float(tds[6].text_content() if tds[6].text_content() != "N/A" else "0"),
          'points_total' : pointsTotal,

          'position' : playerPage.cssselect("div[class='sameHeight1'] table")[0].cssselect("strong")[0].text_content(),
          'team' : playerPage.cssselect("div[class='sameHeight1'] table")[0].cssselect("strong")[1].text_content(),
          'points_last_3_rounds_avg' : float(extraStats[4].cssselect("span[class='value']")[0].text_content() if tds[6].text_content() != "N/A" else "0"),
          'points_highest' : int(extraStats[6].cssselect("span[class='value']")[0].text_content() if tds[6].text_content() != "N/A" else "0"),
          'points_lowest' : int(extraStats[7].cssselect("span[class='value']")[0].text_content() if tds[6].text_content() != "N/A" else "0"),

          'opponent_last_round' : thisRound[1].text_content().strip() if tds[6].text_content() != "N/A" else "",
          'venue_last_round' : thisRound[2].text_content().strip() if tds[6].text_content() != "N/A" else "",
          'price_change_dollar' : int(thisRound[7].text_content().replace('$','').replace(',', '') if tds[6].text_content() != "N/A" else "0"),
          'price_change_percentage' : float(thisRound[8].text_content().replace('%','') if tds[6].text_content() != "N/A" else "0"),

          # placeholder columns
          'points_avg_calc' : int(0),
          'points_last_3_rounds_avg_calc' : int(0)
        }
        print data
    
        scraperwiki.sqlite.save(unique_keys=['name','round','year'], data=data)

def calculateExtraStats(round):
    print "Calculating extra stats for round " + str(round)
    players = scraperwiki.sqlite.select("* from swdata where round=" + str(round))

    for player in players:
        playerName = player['name'].replace("'","''").strip()
        avgCalc = int(player['points_total'])/int(round)
        avgLast3Calc = getPlayerAvgPoints(playerName, int(round)-2, int(round))

        scraperwiki.sqlite.execute("UPDATE swdata" + \
          " SET points_avg_calc="+ str(avgCalc) + ", points_last_3_rounds_avg_calc=" + str(avgLast3Calc) + \
          " WHERE name LIKE '%" + playerName + "%' and round=" + str(round))
        scraperwiki.sqlite.commit()

def getPlayerAvgPoints(playerName, first, last):
    playerInfo = scraperwiki.sqlite.select("* from swdata where name LIKE '%" + playerName + "%' and round<=" + str(last) + " and round >=" + str(first))

    playerAvg = 0
    for thisRound in playerInfo:
        playerAvg += int(thisRound['points_last_round'])
    playerAvg = playerAvg/(last+1 - first)

    return playerAvg 

#do the scraping
#processRounds(rounds)
#for i in range(6,10):
#calculateExtraStats(14)
print "This scraper has been archived."
#!/usr/bin/python

import scraperwiki
import lxml.html
import re
import urllib2

year = "2012"
siteURL = "http://dreamteam.afl.com.au"

rounds = ["/?p=topplayers"]
#rounds = [
#"/?p=topplayers&stats=round&round=1", "/?p=topplayers&stats=round&round=2", "/?p=topplayers&stats=round&round=3",
#"/?p=topplayers&stats=round&round=4", "/?p=topplayers&stats=round&round=5"
#"/?p=topplayers&stats=round&round=6", "/?p=topplayers&stats=round&round=7"
#"/?p=topplayers&stats=round&round=8""/?p=topplayers&stats=round&round=9"
#]

''' Gets links from the given round pages and scrapes them'''
def processRounds(roundURLs):
    for roundURL in roundURLs:
        html = urllib2.urlopen(siteURL + roundURL)
        roundPage = lxml.html.fromstring(html.read())
        html.close()
        
        round = roundPage.cssselect("li[id='tpRound'] a")[0].text_content().replace("round ", "").replace(" Rankings", "").strip()
        print "Round: " + round
        
        roundRows = roundPage.cssselect("div[id='view_standard'] tr")
        # specified in the footer
        pageLinks = roundRows[-1].cssselect("a")
        
        #remove the "next page" link
        del pageLinks[-1]
        
        for link in pageLinks:
            linkURL = siteURL + link.get("href")
            print linkURL
        
            scrapePage(linkURL, round)

        calculateExtraStats(round)

'''Scrapes an individual page'''
def scrapePage(pageURL, round):
    page = lxml.html.fromstring(scraperwiki.scrape(pageURL))
    rows = page.cssselect("div[id='view_standard'] tr")
    
    # remove footer and header row elements
    del rows[0]
    del rows[-1]
    del rows[-1]
    
    for tr in rows:
        tds = tr.cssselect("td")
        ths = tr.cssselect("th")

        # determine data
        playerURL = tds[1].cssselect("a[class='player-name']")[0].get("href")

        #player page info
        playerPage = lxml.html.fromstring(scraperwiki.scrape(siteURL + playerURL))
        roundRows = playerPage.cssselect("table[class='data'] tr")
        extraStats =  playerPage.cssselect("div[class='box']")
        
        roundIndex = int(-1)

        for i, roundRow in enumerate(roundRows):
            rowColumn = roundRow.cssselect("td[class='t1Head2 centered']")

            if (len(rowColumn) != 0 and rowColumn[0].text_content().strip() == round):
                roundIndex = i

        thisRound = roundRows[int(roundIndex)]

        # Variables
        name = tds[1].cssselect("a[class='player-name']")[0].text_content()
        pointsTotal = int(tds[8].text_content().replace(',', ''))

        data = {
          'year' : int(year),
          'round' : int(round),
          'player_id' : int(playerURL.replace('/player/','')),
          'name' : name,
          'price' : int(tds[1].cssselect("strong")[0].text_content().replace('$','').replace(',', '')),
          'games_played' : int(tds[2].text_content()),
          'num_selections' : int(tds[3].text_content().replace(',','')),
          'rank_last_round' : int(re.sub(' \(.+\)','', tds[4].text_content())),
          'mvp_value' : int(tds[5].text_content().replace(',','') if tds[5].text_content() != "N/A" else "0"),
          'points_last_round' : int(tds[7].text_content()),
          'points_avg' : float(tds[6].text_content() if tds[6].text_content() != "N/A" else "0"),
          'points_total' : pointsTotal,

          'position' : playerPage.cssselect("div[class='sameHeight1'] table")[0].cssselect("strong")[0].text_content(),
          'team' : playerPage.cssselect("div[class='sameHeight1'] table")[0].cssselect("strong")[1].text_content(),
          'points_last_3_rounds_avg' : float(extraStats[4].cssselect("span[class='value']")[0].text_content() if tds[6].text_content() != "N/A" else "0"),
          'points_highest' : int(extraStats[6].cssselect("span[class='value']")[0].text_content() if tds[6].text_content() != "N/A" else "0"),
          'points_lowest' : int(extraStats[7].cssselect("span[class='value']")[0].text_content() if tds[6].text_content() != "N/A" else "0"),

          'opponent_last_round' : thisRound[1].text_content().strip() if tds[6].text_content() != "N/A" else "",
          'venue_last_round' : thisRound[2].text_content().strip() if tds[6].text_content() != "N/A" else "",
          'price_change_dollar' : int(thisRound[7].text_content().replace('$','').replace(',', '') if tds[6].text_content() != "N/A" else "0"),
          'price_change_percentage' : float(thisRound[8].text_content().replace('%','') if tds[6].text_content() != "N/A" else "0"),

          # placeholder columns
          'points_avg_calc' : int(0),
          'points_last_3_rounds_avg_calc' : int(0)
        }
        print data
    
        scraperwiki.sqlite.save(unique_keys=['name','round','year'], data=data)

def calculateExtraStats(round):
    print "Calculating extra stats for round " + str(round)
    players = scraperwiki.sqlite.select("* from swdata where round=" + str(round))

    for player in players:
        playerName = player['name'].replace("'","''").strip()
        avgCalc = int(player['points_total'])/int(round)
        avgLast3Calc = getPlayerAvgPoints(playerName, int(round)-2, int(round))

        scraperwiki.sqlite.execute("UPDATE swdata" + \
          " SET points_avg_calc="+ str(avgCalc) + ", points_last_3_rounds_avg_calc=" + str(avgLast3Calc) + \
          " WHERE name LIKE '%" + playerName + "%' and round=" + str(round))
        scraperwiki.sqlite.commit()

def getPlayerAvgPoints(playerName, first, last):
    playerInfo = scraperwiki.sqlite.select("* from swdata where name LIKE '%" + playerName + "%' and round<=" + str(last) + " and round >=" + str(first))

    playerAvg = 0
    for thisRound in playerInfo:
        playerAvg += int(thisRound['points_last_round'])
    playerAvg = playerAvg/(last+1 - first)

    return playerAvg 

#do the scraping
#processRounds(rounds)
#for i in range(6,10):
#calculateExtraStats(14)
print "This scraper has been archived."
#!/usr/bin/python

import scraperwiki
import lxml.html
import re
import urllib2

year = "2012"
siteURL = "http://dreamteam.afl.com.au"

rounds = ["/?p=topplayers"]
#rounds = [
#"/?p=topplayers&stats=round&round=1", "/?p=topplayers&stats=round&round=2", "/?p=topplayers&stats=round&round=3",
#"/?p=topplayers&stats=round&round=4", "/?p=topplayers&stats=round&round=5"
#"/?p=topplayers&stats=round&round=6", "/?p=topplayers&stats=round&round=7"
#"/?p=topplayers&stats=round&round=8""/?p=topplayers&stats=round&round=9"
#]

''' Gets links from the given round pages and scrapes them'''
def processRounds(roundURLs):
    for roundURL in roundURLs:
        html = urllib2.urlopen(siteURL + roundURL)
        roundPage = lxml.html.fromstring(html.read())
        html.close()
        
        round = roundPage.cssselect("li[id='tpRound'] a")[0].text_content().replace("round ", "").replace(" Rankings", "").strip()
        print "Round: " + round
        
        roundRows = roundPage.cssselect("div[id='view_standard'] tr")
        # specified in the footer
        pageLinks = roundRows[-1].cssselect("a")
        
        #remove the "next page" link
        del pageLinks[-1]
        
        for link in pageLinks:
            linkURL = siteURL + link.get("href")
            print linkURL
        
            scrapePage(linkURL, round)

        calculateExtraStats(round)

'''Scrapes an individual page'''
def scrapePage(pageURL, round):
    page = lxml.html.fromstring(scraperwiki.scrape(pageURL))
    rows = page.cssselect("div[id='view_standard'] tr")
    
    # remove footer and header row elements
    del rows[0]
    del rows[-1]
    del rows[-1]
    
    for tr in rows:
        tds = tr.cssselect("td")
        ths = tr.cssselect("th")

        # determine data
        playerURL = tds[1].cssselect("a[class='player-name']")[0].get("href")

        #player page info
        playerPage = lxml.html.fromstring(scraperwiki.scrape(siteURL + playerURL))
        roundRows = playerPage.cssselect("table[class='data'] tr")
        extraStats =  playerPage.cssselect("div[class='box']")
        
        roundIndex = int(-1)

        for i, roundRow in enumerate(roundRows):
            rowColumn = roundRow.cssselect("td[class='t1Head2 centered']")

            if (len(rowColumn) != 0 and rowColumn[0].text_content().strip() == round):
                roundIndex = i

        thisRound = roundRows[int(roundIndex)]

        # Variables
        name = tds[1].cssselect("a[class='player-name']")[0].text_content()
        pointsTotal = int(tds[8].text_content().replace(',', ''))

        data = {
          'year' : int(year),
          'round' : int(round),
          'player_id' : int(playerURL.replace('/player/','')),
          'name' : name,
          'price' : int(tds[1].cssselect("strong")[0].text_content().replace('$','').replace(',', '')),
          'games_played' : int(tds[2].text_content()),
          'num_selections' : int(tds[3].text_content().replace(',','')),
          'rank_last_round' : int(re.sub(' \(.+\)','', tds[4].text_content())),
          'mvp_value' : int(tds[5].text_content().replace(',','') if tds[5].text_content() != "N/A" else "0"),
          'points_last_round' : int(tds[7].text_content()),
          'points_avg' : float(tds[6].text_content() if tds[6].text_content() != "N/A" else "0"),
          'points_total' : pointsTotal,

          'position' : playerPage.cssselect("div[class='sameHeight1'] table")[0].cssselect("strong")[0].text_content(),
          'team' : playerPage.cssselect("div[class='sameHeight1'] table")[0].cssselect("strong")[1].text_content(),
          'points_last_3_rounds_avg' : float(extraStats[4].cssselect("span[class='value']")[0].text_content() if tds[6].text_content() != "N/A" else "0"),
          'points_highest' : int(extraStats[6].cssselect("span[class='value']")[0].text_content() if tds[6].text_content() != "N/A" else "0"),
          'points_lowest' : int(extraStats[7].cssselect("span[class='value']")[0].text_content() if tds[6].text_content() != "N/A" else "0"),

          'opponent_last_round' : thisRound[1].text_content().strip() if tds[6].text_content() != "N/A" else "",
          'venue_last_round' : thisRound[2].text_content().strip() if tds[6].text_content() != "N/A" else "",
          'price_change_dollar' : int(thisRound[7].text_content().replace('$','').replace(',', '') if tds[6].text_content() != "N/A" else "0"),
          'price_change_percentage' : float(thisRound[8].text_content().replace('%','') if tds[6].text_content() != "N/A" else "0"),

          # placeholder columns
          'points_avg_calc' : int(0),
          'points_last_3_rounds_avg_calc' : int(0)
        }
        print data
    
        scraperwiki.sqlite.save(unique_keys=['name','round','year'], data=data)

def calculateExtraStats(round):
    print "Calculating extra stats for round " + str(round)
    players = scraperwiki.sqlite.select("* from swdata where round=" + str(round))

    for player in players:
        playerName = player['name'].replace("'","''").strip()
        avgCalc = int(player['points_total'])/int(round)
        avgLast3Calc = getPlayerAvgPoints(playerName, int(round)-2, int(round))

        scraperwiki.sqlite.execute("UPDATE swdata" + \
          " SET points_avg_calc="+ str(avgCalc) + ", points_last_3_rounds_avg_calc=" + str(avgLast3Calc) + \
          " WHERE name LIKE '%" + playerName + "%' and round=" + str(round))
        scraperwiki.sqlite.commit()

def getPlayerAvgPoints(playerName, first, last):
    playerInfo = scraperwiki.sqlite.select("* from swdata where name LIKE '%" + playerName + "%' and round<=" + str(last) + " and round >=" + str(first))

    playerAvg = 0
    for thisRound in playerInfo:
        playerAvg += int(thisRound['points_last_round'])
    playerAvg = playerAvg/(last+1 - first)

    return playerAvg 

#do the scraping
#processRounds(rounds)
#for i in range(6,10):
#calculateExtraStats(14)
print "This scraper has been archived."
