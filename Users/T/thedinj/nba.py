#Scrapes Fox Sports NBA game data
#Thunder/Grizz on 3/27/11 is missing from the play-by-play
import scraperwiki
import urlparse
import lxml.html
import re
from datetime import datetime, timedelta

def scrapeSchedule(scheduleUrl, seasonFrYr, seasonToYr, gameIDs):
    print "Scraping schedule from '{0}'...".format(scheduleUrl)
    html = scraperwiki.scrape(scheduleUrl)
    root = lxml.html.fromstring(html)
    rows = []
    rows.extend(root.cssselect("table.dataTbl tr.dataTr"))  #Data is zebra-striped
    rows.extend(root.cssselect("table.dataTbl tr.dataTr2"))
    if not rows:
        return
    for row in rows:
        cells = row.cssselect("td")
        if not cells:
            continue
        gameDate = getGameDate(cleanString(cells[0].text_content()), seasonFrYr, seasonToYr)
        if not gameDate:
            continue
        links = row.cssselect("a")
        if not links:
            continue
        for link in links:
            href = link.attrib["href"]
            queryString = urlparse.urlparse(href).query
            query = urlparse.parse_qs(queryString)
            if query.has_key("gameId"):  #Game links contain gameId=xxxx querystring parameters
                gameId = query["gameId"][0]
                gameIDs[gameId] = gameDate  #Store an entry in the dictionary

def cleanUpGame(gameId):
    scraperwiki.sqlite.execute("delete from Games where gameId=?", gameId)
    scraperwiki.sqlite.execute("delete from PlayByPlays where gameId=?", gameId)
    return        

def scrapeGame(gameId, season, gameDate):
    if not gameIsComplete(gameDate):
        #cleanup just in case
        cleanUpGame(gameId)
        return
    res = None
    try:
        res = scraperwiki.sqlite.select("gameId from Games where gameId=?", gameId)
    except:
        pass
    if res:
        if len(res) > 0:
            #if not gameId.startswith('20110406'):  #junked up games listed here (temporarily)
            #print "Already got data for gameId ",gameId
            return 0 #already got it

    cleanUpGame(gameId)

    teams = getTeams(gameId)
    if not teams:
        return 0
    pbpRecords = scrapePlayByPlay(gameId, teams["awayTeam"], teams["homeTeam"])  #For testing a single game, comment-out above loop and uncomment this
    if pbpRecords == None:
        return 0
    scraperwiki.sqlite.save(['season', 'gameId'], {"season": season, "gameId": gameId, "gameDate": gameDate, "awayTeam": teams["awayTeam"], "homeTeam": teams["homeTeam"]}, 'Games')
    scraperwiki.sqlite.save(['gameId','recordId'], pbpRecords, 'PlayByPlays')
    return 1

def getTeams(gameId):
    gameUrl = "http://msn.foxsports.com/nba/gameTrax?gameId={0}".format(gameId)
    print "Determining teams from {0}...".format(gameUrl)
    html = scraperwiki.scrape(gameUrl)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table.sbTeamsBg tr.sbTeam")
    awayTeam = None
    homeTeam = None
    if not rows:
        return None;
    for row in rows:
        cells = row.cssselect("td")
        if not cells:
            continue
        cellTeam = getTeamInfo(cleanString(cells[0].text_content()))["city"]
        if awayTeam == None:
            awayTeam = cellTeam
            continue
        if homeTeam == None:
            homeTeam = cellTeam
            break
    if awayTeam == None or homeTeam == None:
        return None
    return { "awayTeam": awayTeam, "homeTeam": homeTeam }

def scrapePlayByPlay(gameId, awayTeam, homeTeam):
    gameUrl = "http://msn.foxsports.com/nba/playbyplay?gameId={0}&refreshRate=off".format(gameId)
    print "Scraping game data from '{0}'...".format(gameUrl)
    html = scraperwiki.scrape(gameUrl)
    root = lxml.html.fromstring(html)
    rows = root.cssselect("table.bgBdr tr")
    records = []
    currentPeriod = None  #Hopefully never see this in real data.
    nextUpdate = None     #Should never occur in real data either
    recordId = 0
    for row in rows:
        cells = row.cssselect("td")
        if not cells:
            continue
        if row.attrib["class"] == "bgC":  #Regular gameflow data
            gameMMSS = cleanString(cells[0].text_content())

            time = getNormalizedGameTime(currentPeriod, gameMMSS)

            score = parseScore(cleanString(cells[4].text_content()), awayTeam, homeTeam)
            if not score:
                continue

            team = getTeamInfo(cleanString(cells[1].text_content()))
            if not team:
                continue
            
            recordId += 1

            record = {}
            record['gameId'] = gameId
            record['recordId'] = recordId
            record['team'] = team['city']
            record['player'] = cleanString(cells[2].text_content())
            record['action'] = cleanString(cells[3].text_content())
            record['homeTeamScore'] = score['homeTeamScore']
            record['awayTeamScore'] = score['awayTeamScore']
            record['time'] = time
            record['nextUpdate'] = nextUpdate

            if nextUpdate < time:
                #in practice, these aren't that bad (a couple seconds of skew)
                continue #to the next row

            nextUpdate = record['time']

            records.append(record)

        elif row.attrib["class"] == "bgHdr1":  #Periods
            cell = cells[0]
            if cell != None:

                #Get rid of the links to other quarters
                spans = cell.cssselect("span")
                if spans:
                    span = spans[0]
                    if span != None:
                        span.drop_tree()

                periodName = cleanString(cell.text_content())

                if currentPeriod == None:
                    periodInfo = getPeriodInfo(periodName)
                    nextUpdate = periodInfo["offset"] + periodInfo["length"] #Set as end of the game

                currentPeriod = periodName #Set the current period
    if len(records) < 1:
        print "ERROR: < 1 record"
        return None #Something bad happened

    print "Success."

    return records

def parseScore(scoreString, awayTeam, homeTeam):
    teamAndScore = scoreString.split(' ')
    teamString = teamAndScore[0]
    score = teamAndScore[1].split('-')
    leadingTeam = getTeamInfo(teamString)["city"]
    if not leadingTeam:
        return None
    if leadingTeam == homeTeam:
        return { "homeTeamScore": score[0], "awayTeamScore": score[1] }
    if leadingTeam == awayTeam:
        return { "homeTeamScore": score[1], "awayTeamScore": score[0] }
    return None

def cleanString(string):
    return string.replace('\n', '').strip()

def getPeriodInfo(periodName):
    offset = 0
    length = 0

    if periodName == "1st Quarter":
        offset = 0
        length = 720
    elif periodName == "2nd Quarter":
        offset = 720
        length = 720
    elif periodName == "3rd Quarter":
        offset = 1440
        length = 720
    elif periodName == "4th Quarter":
        offset = 2160
        length = 720
    elif periodName == "Overtime":
        offset = 2880
        length = 300
    elif periodName == "Double Overtime":
        offset = 3180
        length = 300
    elif periodName == "Triple Overtime":
        offset = 3580
        length = 300
    elif periperiodName == "Quadruple Overtime":
        offset = 4180
        length = 300
    else:
        print "ERROR Unexpected quarter found: ", periodName
        #hopefully don't ever need more

    return {"offset" : offset, "length": length}

def getTeamInfo(teamString):
    teamString = teamString.upper()

    if teamString == "76ERS" or teamString == "PHI":
        return { "nickname": "76ers", "city": "Phi" }
    if teamString == "BOBCATS" or teamString == "CHA":
        return { "nickname": "Bobcats", "city": "Cha" }
    if teamString == "BUCKS" or teamString == "MIL":
        return { "nickname": "Bucks", "city": "Mil" }
    if teamString == "BULLS" or teamString == "CHI":
        return { "nickname": "Bulls", "city": "Chi" }
    if teamString == "CAVALIERS" or teamString == "CLE":
        return { "nickname": "Cavaliers", "city": "Cle" }
    if teamString == "CELTICS" or teamString == "BOS":
        return { "nickname": "Celtics", "city": "Bos" }
    if teamString == "CLIPPERS" or teamString == "LAC":
        return { "nickname": "Clippers", "city": "LAC" }
    if teamString == "GRIZZLIES" or teamString == "MEM":
        return { "nickname": "Grizzlies", "city": "Mem" }
    if teamString == "HAWKS" or teamString == "ATL":
        return { "nickname": "Hawks", "city": "Atl" }
    if teamString == "HEAT" or teamString == "MIA":
        return { "nickname": "Heat", "city": "Mia" }
    if teamString == "HORNETS" or teamString == "NO":
        return { "nickname": "Hornets", "city": "NO" }
    if teamString == "JAZZ" or teamString == "UTA":
        return { "nickname": "Jazz", "city": "Uta" }
    if teamString == "KINGS" or teamString == "SAC":
        return { "nickname": "Kings", "city": "Sac" }
    if teamString == "KNICKS" or teamString == "NY":
        return { "nickname": "Knicks", "city": "NY" }
    if teamString == "LAKERS" or teamString == "LAL":
        return { "nickname": "Lakers", "city": "LAL" }
    if teamString == "MAGIC" or teamString == "ORL":
        return { "nickname": "Magic", "city": "Orl" }
    if teamString == "MAVERICKS" or teamString == "DAL":
        return { "nickname": "Mavericks", "city": "Dal" }
    if teamString == "NETS" or teamString == "BKN":
        return { "nickname": "Nets", "city": "BKN" }
    if teamString == "NUGGETS" or teamString == "DEN":
        return { "nickname": "Nuggets", "city": "Den" }
    if teamString == "PACERS" or teamString == "IND":
        return { "nickname": "Pacers", "city": "Ind" }
    if teamString == "PISTONS" or teamString == "DET":
        return { "nickname": "Pistons", "city": "Det" }
    if teamString == "RAPTORS" or teamString == "TOR":
        return { "nickname": "Raptors", "city": "Tor" }
    if teamString == "ROCKETS" or teamString == "HOU":
        return { "nickname": "Rockets", "city": "Hou" }
    if teamString == "SPURS" or teamString == "SA":
        return { "nickname": "Spurs", "city": "SA" }
    if teamString == "SUNS" or teamString == "PHO":
        return { "nickname": "Suns", "city": "Pho" }
    if teamString == "THUNDER" or teamString == "OKC":
        return { "nickname": "Thunder", "city": "OKC" }
    if teamString == "TIMBERWOLVES" or teamString == "MIN":
        return { "nickname": "Timberwolves", "city": "Min" }
    if teamString == "TRAIL BLAZERS" or teamString == "POR":
        return { "nickname": "Trail Blazers", "city": "Por" }
    if teamString == "WARRIORS" or teamString == "GS":
        return { "nickname": "Warriors", "city": "GS" }
    if teamString == "WIZARDS" or teamString == "WAS":
        return { "nickname": "Wizards", "city": "Was" }

    print "ERROR: Unrecognized team: ", teamString

    return { "nickname": None, "city": None }

def getNormalizedGameTime(periodName, time):
    #determine a period offset
    periodInfo = getPeriodInfo(periodName)

    #now get the time in the period
    minsSecs = time.split(":")
    mins = int(minsSecs[0].replace(' ',''))
    secs = int(minsSecs[1].replace(' ',''))
    
    return periodInfo["offset"] + (periodInfo["length"] - ((60 * mins) + secs))  #period offset plus time elapsed in period

MAX_GAMES_PER_RUN = 300

def scrapeSchedules(seasonUrl, seasonFrYr, seasonToYr):
    seasonName = '{0}-{1}'.format(seasonFrYr, seasonToYr)
    print "Scraping schedule URLs for the {0} season from '{1}'...".format(seasonName, seasonUrl)
    html = scraperwiki.scrape(seasonUrl)
    root = lxml.html.fromstring(html)
    links = root.cssselect("div.teamLinks a")
    scheduleUrls = []
    for link in links:
        if cleanString(link.text_content()).upper() == "SCHEDULE":
            href = urlparse.urljoin('http://msn.foxsports.com',link.attrib["href"])
            scheduleUrls.append(href)
#    scheduleUrls.append('http://msn.foxsports.com/nba/team/milwaukee-bucks/schedule/71089') #debug--Bucks 2010-2011
    gameIDs = {}
    for scheduleUrl in scheduleUrls:
        scrapeSchedule(scheduleUrl, seasonFrYr, seasonToYr, gameIDs)
    gamesScraped = 0
    for gameId in gameIDs.keys():
        gameDate = gameIDs[gameId]
        if(scrapeGame(gameId, seasonName, gameDate)):
            gamesScraped = gamesScraped + 1
            if gamesScraped >= MAX_GAMES_PER_RUN:
                break

def getGameDate(dateString, seasonFrYr, seasonToYr):
    try:
        gameDate = datetime.strptime(dateString, '%A, %b %d')
    except:
        return None
    if gameDate.month > 9:
        gameDate = datetime(seasonFrYr, gameDate.month, gameDate.day)
    else:
        gameDate = datetime(seasonToYr, gameDate.month, gameDate.day)
    return gameDate

def gameIsComplete(gameDate):
    now = datetime.today()  #Server appears to be on UTC
    checkDate = (now - timedelta(hours=10)).date()
    return gameDate.date() < checkDate

def main():    
    scrapeSchedules('http://msn.foxsports.com/nba/teams', 2010, 2011)
    
main()