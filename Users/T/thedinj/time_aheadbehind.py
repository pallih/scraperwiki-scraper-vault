#Led/trailed by 10, 20
#wins/losses in separate columns
import scraperwiki.sqlite

HOME = 1
AWAY = 2

SHOW_WINS = 1
SHOW_LOSSES = 2

SHOW_MORE_WINNING = 1
SHOW_MORE_LOSING = 2
SHOW_EQUAL_TIME = 3

SHOW_NEVER_TRAILING = 1
SHOW_NEVER_LEADING = 2

cachedGames = {}

seasonTotalsRows = []
homeTotalsRows = []
awayTotalsRows = []
winsTotalsRows = []
lossesTotalsRows = []
moreWinningTotalsRows = []
moreLosingTotalsRows = []
equalTimeTotalsRows = []
recentTotalsRows = []
neverTrailingTotalRows = []
neverLeadingTotalRows = []

class GameData:
    gameId = ''
    homeTeam = ''
    awayTeam = ''
    date = ''
    homeTeamAheadTime = 0
    awayTeamAheadTime = 0
    teamsTiedTime = 0
    totalTime = 0
    homeTeamScore = 0
    awayTeamScore = 0

def formatTime(numSeconds):
    minutes = int(numSeconds / 60)
    remainder = numSeconds % 60
    return "{0}:{1:02d}".format(minutes, remainder)

def formatPercent(numerator, denominator):
    if denominator == 0:
        return "N/A"
    return '{0:.2%}'.format(numerator/float(denominator))

def getTeamGames(season, team):
    gameList= []
    sdata = scraperwiki.sqlite.execute("select gameId,gameDate,homeTeam,awayTeam from src.Games where season=? and homeTeam=? or awayTeam=? order by gameDate asc", [season, team, team])
    rows = sdata.get("data")
    gameList= []
    for row in rows:
        gameId = row[0]
        if cachedGames.has_key(gameId):  #check the cache
            gameData = cachedGames[gameId]
            gameList.append(gameData)
        else:
            gameData = GameData()
            gameData.gameId = gameId
            gameData.date = row[1]
            gameData.homeTeam = row[2]
            gameData.awayTeam = row[3]
            if calcGameData(gameData):
                gameList.append(gameData)
                cachedGames[gameId] = gameData  #cache it
    return gameList

def calcGameData(gameData):
    sdata = scraperwiki.sqlite.execute("select awayTeamScore,homeTeamScore,time,nextUpdate from src.PlayByPlays where gameId=? order by recordId desc", [gameData.gameId])
    rows = sdata.get("data")
    
    for row in rows:
        time = int(row[2])
        nextUpdate = int(row[3])
        timeDiff = int(nextUpdate) - int(time)
        if timeDiff <= 0:
            continue
        awayTeamScore = int(row[0])
        homeTeamScore = int(row[1])
        scoreDiff = int(awayTeamScore) - int(homeTeamScore)
        if scoreDiff == 0:
            gameData.teamsTiedTime += timeDiff
        elif scoreDiff > 0:
            gameData.awayTeamAheadTime += timeDiff
        else: #scoreDiff < 0
            gameData.homeTeamAheadTime += timeDiff
        gameData.totalTime += timeDiff
    lastrow = rows[-1]
    gameData.homeTeamScore = int(lastrow[1]) 
    gameData.awayTeamScore = int(lastrow[0])

    #sanity checks
    if (gameData.homeTeamScore == gameData.awayTeamScore) or (gameData.totalTime < 2880):
        print "INVALID GAME DATA IN gameId {0}<br>".format(gameData.gameId)
        return 0   

    return 1

def getTeamCell(cellData, teamIsHome, statIsHome, isWin):
    markupBegin = ""
    markupEnd = ""
    if (teamIsHome and statIsHome) or ((not teamIsHome) and (not statIsHome)):
        if isWin:
            markupBegin = ' style="background-color:#99FF00"'
            markupEnd = "" #not used
        else:
            markupBegin = ' style="background-color:#FF9966"'
            markupEnd = "" #not used
    return "<td{0}>{1}{2}</td>".format(markupBegin, cellData, markupEnd)    

def printGameList(season, team, gameList, caption):
    print '<h2>{0}</2>'.format(caption)
    print '<table border="1" style="border-collapse:collapse;">'
    
    # column headings
    print "<tr>"
    print "<th>Game #</th>"
    print "<th>Away Team</th>"
    print "<th>Home Team</th>"
    print "<th>Result</th>"
    print "<th>Record</th>"
    print "<th>Winning %</th>"
    print "<th>Away Team Ahead (time)</th>"
    print "<th>Away Team Ahead (%)</th>"
    print "<th>Home Team Ahead (time)</th>"
    print "<th>Home Team Ahead (%)</th>"
    print "<th>Teams Tied (time)</th>"
    print "<th>Teams Tied (%)</th>"
    print "<th>Total (time)</th>"
    print "</tr>"
    
    # rows
    gameNum = 0
    wins = 0
    losses = 0
    for game in gameList:
        gameNum+=1
        teamIsHome = (game.homeTeam == team)
        if teamIsHome:
            isWin = (game.homeTeamScore > game.awayTeamScore)
        else:
            isWin = (game.awayTeamScore > game.homeTeamScore)
        if isWin:
            result = "W"
            wins += 1
        else:
            result = "L"
            losses += 1

        print "<tr>"
        print getTeamCell(gameNum, 1, 0, isWin) 
        print getTeamCell("{0} ({1})".format(game.awayTeam, game.awayTeamScore), teamIsHome, 0, isWin)
        print getTeamCell("{0} ({1})".format(game.homeTeam, game.homeTeamScore), teamIsHome, 1, isWin)
        print getTeamCell(result, teamIsHome, teamIsHome, isWin)
        print getTeamCell("{0}-{1}".format(wins, losses), 1, 0, isWin)
        print getTeamCell(formatPercent(wins, gameNum), 1, 0, isWin)
        print getTeamCell(formatTime(game.awayTeamAheadTime), teamIsHome, 0, isWin)
        print getTeamCell(formatPercent(game.awayTeamAheadTime, game.totalTime), teamIsHome, 0, isWin)
        print getTeamCell(formatTime(game.homeTeamAheadTime), teamIsHome, 1, isWin)
        print getTeamCell(formatPercent(game.homeTeamAheadTime, game.totalTime), teamIsHome, 1, isWin)
        print getTeamCell(formatTime(game.teamsTiedTime), 1, 0, isWin)
        print getTeamCell(formatPercent(game.teamsTiedTime, game.totalTime), 1, 0, isWin)
        print getTeamCell(formatTime(game.totalTime), 1, 0, isWin)
        print "</tr>"
        
    print "</table>"

def getTotals(rows, gameList, team):
    teamAheadTime = 0
    teamBehindTime = 0
    teamTiedTime = 0
    totalTime = 0
    gameCount = 0
    wins = 0
    losses = 0
    pointsFor = 0
    pointsAgainst = 0
    totalPoints = 0

    for game in gameList:
        if game.awayTeam == team:
            teamAheadTime += game.awayTeamAheadTime
            teamBehindTime += game.homeTeamAheadTime
            isWin = (game.awayTeamScore > game.homeTeamScore)
            pointsFor += game.awayTeamScore
            pointsAgainst += game.homeTeamScore
        else: #if game.homeTeam == team
            teamAheadTime += game.homeTeamAheadTime
            teamBehindTime += game.awayTeamAheadTime
            isWin = (game.homeTeamScore > game.awayTeamScore)
            pointsFor += game.homeTeamScore
            pointsAgainst += game.awayTeamScore
        if isWin:
            wins += 1
        else:
            losses += 1          
            
        teamTiedTime += game.teamsTiedTime
        totalTime += game.totalTime
        totalPoints += game.homeTeamScore
        totalPoints += game.awayTeamScore
        gameCount += 1
    
    rows.append([team, gameCount, wins, losses, formatPercent(wins, wins+losses), pointsFor, formatPercent(pointsFor, totalPoints), pointsAgainst, formatPercent(pointsAgainst, totalPoints), totalPoints, formatTime(teamAheadTime), formatPercent(teamAheadTime, totalTime), formatTime(teamBehindTime), formatPercent(teamBehindTime, totalTime), formatTime(teamTiedTime), formatPercent(teamTiedTime, totalTime), formatTime(totalTime)])

def getLocGames(rows, gameList, team, show):
    subGameList = []
    for game in gameList:
        if show == HOME:
            if game.homeTeam == team:
                subGameList.append(game)
        else: #show == AWAY:
            if game.awayTeam == team:
                subGameList.append(game)
    getTotals(rows, subGameList, team)

def getResultGames(rows, gameList, team, show):
    subGameList = []
    for game in gameList:
        teamIsHome = (game.homeTeam == team)
        if teamIsHome:
            isWin = (game.homeTeamScore > game.awayTeamScore)
        else:
            isWin = (game.awayTeamScore > game.homeTeamScore)
        if (isWin and (show == SHOW_WINS)) or ((not isWin) and (show == SHOW_LOSSES)):
            subGameList.append(game)
    getTotals(rows, subGameList, team)

def getRecentGames(rows, gameList, team, max):
    subGameList = []
    if max > len(gameList):
        max = gameList
    for index in range(-max, 0):
        game = gameList[index]
        subGameList.append(game)
    getTotals(rows, subGameList, team)

def getTimeDiffGames(rows, gameList, team, show):
    subGameList = []
    for game in gameList:
        if game.homeTeam == team:
            if game.awayTeamAheadTime > game.homeTeamAheadTime:
                moreLosing = 1
                moreWinning = 0
            elif game.homeTeamAheadTime > game.awayTeamAheadTime:
                moreLosing = 0
                moreWinning = 1
            else:
                moreLosing = 0
                moreWinning = 0
        else: #game.awayTeam == team
            if game.homeTeamAheadTime > game.awayTeamAheadTime:
                moreLosing = 1
                moreWinning = 0
            elif game.awayTeamAheadTime > game.homeTeamAheadTime:
                moreLosing = 0
                moreWinning = 1
            else:
                moreLosing = 0
                moreWinning = 0
        if (show == SHOW_MORE_WINNING) and moreWinning:
            subGameList.append(game)        
        elif (show == SHOW_MORE_LOSING) and moreLosing:
            subGameList.append(game)
        elif (show == SHOW_EQUAL_TIME) and (not moreWinning) and (not moreLosing):
            subGameList.append(game)    
    getTotals(rows, subGameList, team)

def getNeverTrailedLedGames(rows, gameList, team, show):
    subGameList = []
    for game in gameList:
        if game.homeTeam == team:
            if game.awayTeamAheadTime == 0:
                neverTrailing = 1
                neverLeading = 0
            elif game.homeTeamAheadTime == 0:
                neverTrailing = 0
                neverLeading = 1
            else:
                neverTrailing = 0
                neverLeading = 0
        else: #game.awayTeam == team
            if game.homeTeamAheadTime == 0:
                neverTrailing = 1
                neverLeading = 0
            elif game.awayTeamAheadTime == 0:
                neverTrailing = 0
                neverLeading = 1
            else:
                neverTrailing = 0
                neverLeading = 0
        if (show == SHOW_NEVER_TRAILING ) and neverTrailing:
            subGameList.append(game)        
        elif (show == SHOW_NEVER_LEADING) and neverLeading:
            subGameList.append(game)
    getTotals(rows, subGameList, team)

def getTeams(season):
    for key in ["awayTeam", "homeTeam"]:
        sdata = scraperwiki.sqlite.execute("select distinct {0} from src.Games where season=?".format(key), [season])
        rows = sdata.get("data")
        teamDic = {}
        for row in rows:
            teamDic[row[0]] = ""
    teams = []
    for team in teamDic.keys():
        teams.append(team)
    return teams

def showTeamData(season, team):    
    gameList = getTeamGames(season, team)
    
    #print '<h1>Results for {0} in {1}</h1>'.format(team, season)
    #printGameList(season, team, gameList, "Game Totals")

    getTotals(seasonTotalsRows, gameList, team)
    getLocGames(homeTotalsRows, gameList, team, HOME)
    getLocGames(awayTotalsRows, gameList, team, AWAY)
    getResultGames(winsTotalsRows, gameList, team, SHOW_WINS)
    getResultGames(lossesTotalsRows, gameList, team, SHOW_LOSSES)
    getTimeDiffGames(moreWinningTotalsRows, gameList, team, SHOW_MORE_WINNING)
    getTimeDiffGames(moreLosingTotalsRows, gameList, team, SHOW_MORE_LOSING)
    getTimeDiffGames(equalTimeTotalsRows, gameList, team, SHOW_EQUAL_TIME)
    getRecentGames(recentTotalsRows, gameList, team, 10)
    getNeverTrailedLedGames(neverTrailingTotalRows, gameList, team, SHOW_NEVER_TRAILING)
    getNeverTrailedLedGames(neverLeadingTotalRows, gameList, team, SHOW_NEVER_LEADING)

def printTable(caption, cols, rows):
    print '<h2>{0}</h2>'.format(caption)
    print '<table border="1" style="border-collapse:collapse;">'
    
    # column headings
    print "<tr>"
    for col in cols:
        print "<th>{0}</th>".format(col)
    print "</tr>"
    
    # rows
    for row in rows:
        print "<tr>"
        for cell in row:
            print "<td>{0}</td>".format(cell)
        print "</tr>"
        
    print "</table>"

def printTotalsTable(rows, caption):
    cols = ["Team", "Games", "Wins", "Losses", "Winning %", "Points For", "Points For (%/Total)", "Points Against", "Points Against (%/Total)", "Total Points", "Team Ahead (time)", "Team Ahead (%)", "Team Behind (time)", "Team Behind (%)", "Team Tied (time)", "Team Tied (%)", "Total Time"]
    printTable(caption, cols, rows)

def main():
    scraperwiki.sqlite.attach("nba", "src")
    season = u'2010-2011'
    teams = getTeams(season)

    for team in teams:
        showTeamData(season, team)
#    showTeamData(season, "Mil")
#    showTeamData(season, "Chi")
    
    printTotalsTable(seasonTotalsRows, "Season Totals")
    #printTotalsTable(homeTotalsRows, "Home Game Totals")
    #printTotalsTable(awayTotalsRows, "Away Game Totals")
    #printTotalsTable(winsTotalsRows, "Wins Totals")
    #printTotalsTable(lossesTotalsRows, "Losses Totals")
    printTotalsTable(moreWinningTotalsRows, "Winning Time > Losing Time Totals")
    printTotalsTable(moreLosingTotalsRows, "Losing Time > Winning Time Totals")
    #printTotalsTable(equalTimeTotalsRows, "Winning Time = Losing Time Totals")
    #printTotalsTable(recentTotalsRows, "Recent Game Totals")
    #printTotalsTable(neverTrailingTotalRows, "Never Trailing Game Totals")
    #printTotalsTable(neverLeadingTotalRows, "Never Leading Game Totals")

main()

