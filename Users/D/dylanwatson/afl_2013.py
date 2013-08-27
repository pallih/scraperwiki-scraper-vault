#!/usr/bin/python

import scraperwiki
import lxml.html
import re
import urllib2
import httplib

year = "2013"
siteURL = "http://dreamteam.afl.com.au"

pages = ["/?p=topplayers"]

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

'''Returns the default value unless if is equal to the notThis value in which case it returns the alternative'''
def defaultValue(default, notThis, alternative):
    return default if default != notThis else alternative

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
        print playerURL

        #player page info
        url = siteURL + playerURL
        try:
            playerPage = lxml.html.fromstring(scraperwiki.scrape(url))

        # this should be just catching BadStatusLine but I have been unable to import it
        except Exception:
            print "could not fetch %s, trying again in 10 seconds" % url
            time.sleep(10)
            playerPage = lxml.html.fromstring(scraperwiki.scrape(url))

        roundRows = playerPage.cssselect("table[id='player_profile_next_opp_table'] tr")

        extraStats =  playerPage.cssselect("div[class='box']")
        
        roundIndex = int(-1)
        for i, roundRow in enumerate(roundRows):
            rowColumn = roundRow.cssselect("td[class='t1Head2 centered']")
        
            if (len(rowColumn) != 0 and rowColumn[0].text_content().strip() == round):
                roundIndex = i
                print i

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
          'mvp_value' : int(defaultValue(tds[5].text_content().replace(',',''), "N/A","0")),
          'points_last_round' : int(tds[7].text_content()),
          'points_avg' : float(defaultValue(tds[6].text_content(), "N/A", "0")),
          'points_total' : pointsTotal,

          'position' : playerPage.cssselect("div[class='colTwo'] td")[2].text_content().replace('POSITION','').strip(),
          'team' : playerPage.cssselect("div[class='colTwo'] td")[1].text_content().replace('TEAM','').strip(),
          #'points_last_3_rounds_avg' : float(defaultValue(extraStats[8].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),
          #'points_last_5_rounds_avg' : float(defaultValue(extraStats[9].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),
          #'points_highest' : int(defaultValue(extraStats[10].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),
          #'points_lowest' : int(defaultValue(extraStats[11].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),

          #TODO Uncomment these after round 1
          'opponent_last_round' : "", #thisRound[1].text_content().strip(),
          'venue_last_round' : "", #thisRound[2].text_content().strip(),
          #'price_change_dollar' : int(defaultValue(thisRound[7].text_content().replace('$','').replace(',', ''), "&middot;", "0")),
          #'price_change_percentage' : float(defaultValue(thisRound[8].text_content().replace('%',''), "&middot;", "0")),
        }
        print data
    
        scraperwiki.sqlite.save(unique_keys=['name','round','year'], data=data)

#do the scraping
processRounds(pages)#!/usr/bin/python

import scraperwiki
import lxml.html
import re
import urllib2
import httplib

year = "2013"
siteURL = "http://dreamteam.afl.com.au"

pages = ["/?p=topplayers"]

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

'''Returns the default value unless if is equal to the notThis value in which case it returns the alternative'''
def defaultValue(default, notThis, alternative):
    return default if default != notThis else alternative

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
        print playerURL

        #player page info
        url = siteURL + playerURL
        try:
            playerPage = lxml.html.fromstring(scraperwiki.scrape(url))

        # this should be just catching BadStatusLine but I have been unable to import it
        except Exception:
            print "could not fetch %s, trying again in 10 seconds" % url
            time.sleep(10)
            playerPage = lxml.html.fromstring(scraperwiki.scrape(url))

        roundRows = playerPage.cssselect("table[id='player_profile_next_opp_table'] tr")

        extraStats =  playerPage.cssselect("div[class='box']")
        
        roundIndex = int(-1)
        for i, roundRow in enumerate(roundRows):
            rowColumn = roundRow.cssselect("td[class='t1Head2 centered']")
        
            if (len(rowColumn) != 0 and rowColumn[0].text_content().strip() == round):
                roundIndex = i
                print i

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
          'mvp_value' : int(defaultValue(tds[5].text_content().replace(',',''), "N/A","0")),
          'points_last_round' : int(tds[7].text_content()),
          'points_avg' : float(defaultValue(tds[6].text_content(), "N/A", "0")),
          'points_total' : pointsTotal,

          'position' : playerPage.cssselect("div[class='colTwo'] td")[2].text_content().replace('POSITION','').strip(),
          'team' : playerPage.cssselect("div[class='colTwo'] td")[1].text_content().replace('TEAM','').strip(),
          #'points_last_3_rounds_avg' : float(defaultValue(extraStats[8].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),
          #'points_last_5_rounds_avg' : float(defaultValue(extraStats[9].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),
          #'points_highest' : int(defaultValue(extraStats[10].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),
          #'points_lowest' : int(defaultValue(extraStats[11].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),

          #TODO Uncomment these after round 1
          'opponent_last_round' : "", #thisRound[1].text_content().strip(),
          'venue_last_round' : "", #thisRound[2].text_content().strip(),
          #'price_change_dollar' : int(defaultValue(thisRound[7].text_content().replace('$','').replace(',', ''), "&middot;", "0")),
          #'price_change_percentage' : float(defaultValue(thisRound[8].text_content().replace('%',''), "&middot;", "0")),
        }
        print data
    
        scraperwiki.sqlite.save(unique_keys=['name','round','year'], data=data)

#do the scraping
processRounds(pages)#!/usr/bin/python

import scraperwiki
import lxml.html
import re
import urllib2
import httplib

year = "2013"
siteURL = "http://dreamteam.afl.com.au"

pages = ["/?p=topplayers"]

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

'''Returns the default value unless if is equal to the notThis value in which case it returns the alternative'''
def defaultValue(default, notThis, alternative):
    return default if default != notThis else alternative

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
        print playerURL

        #player page info
        url = siteURL + playerURL
        try:
            playerPage = lxml.html.fromstring(scraperwiki.scrape(url))

        # this should be just catching BadStatusLine but I have been unable to import it
        except Exception:
            print "could not fetch %s, trying again in 10 seconds" % url
            time.sleep(10)
            playerPage = lxml.html.fromstring(scraperwiki.scrape(url))

        roundRows = playerPage.cssselect("table[id='player_profile_next_opp_table'] tr")

        extraStats =  playerPage.cssselect("div[class='box']")
        
        roundIndex = int(-1)
        for i, roundRow in enumerate(roundRows):
            rowColumn = roundRow.cssselect("td[class='t1Head2 centered']")
        
            if (len(rowColumn) != 0 and rowColumn[0].text_content().strip() == round):
                roundIndex = i
                print i

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
          'mvp_value' : int(defaultValue(tds[5].text_content().replace(',',''), "N/A","0")),
          'points_last_round' : int(tds[7].text_content()),
          'points_avg' : float(defaultValue(tds[6].text_content(), "N/A", "0")),
          'points_total' : pointsTotal,

          'position' : playerPage.cssselect("div[class='colTwo'] td")[2].text_content().replace('POSITION','').strip(),
          'team' : playerPage.cssselect("div[class='colTwo'] td")[1].text_content().replace('TEAM','').strip(),
          #'points_last_3_rounds_avg' : float(defaultValue(extraStats[8].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),
          #'points_last_5_rounds_avg' : float(defaultValue(extraStats[9].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),
          #'points_highest' : int(defaultValue(extraStats[10].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),
          #'points_lowest' : int(defaultValue(extraStats[11].cssselect("span[class='value']")[0].text_content(), "N/A", "0")),

          #TODO Uncomment these after round 1
          'opponent_last_round' : "", #thisRound[1].text_content().strip(),
          'venue_last_round' : "", #thisRound[2].text_content().strip(),
          #'price_change_dollar' : int(defaultValue(thisRound[7].text_content().replace('$','').replace(',', ''), "&middot;", "0")),
          #'price_change_percentage' : float(defaultValue(thisRound[8].text_content().replace('%',''), "&middot;", "0")),
        }
        print data
    
        scraperwiki.sqlite.save(unique_keys=['name','round','year'], data=data)

#do the scraping
processRounds(pages)