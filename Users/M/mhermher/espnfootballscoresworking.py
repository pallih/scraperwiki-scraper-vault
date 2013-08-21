import scraperwiki

# Blank Python
import urllib
import re
gID = 1
year = 2011
playid = 1
while year < 2012:
    w = 1
    while w<18:
        #open url copy to "pageread" and close
        page = urllib.urlopen("http://scores.espn.go.com/nfl/scoreboard?seasonYear="+str(year)+"&seasonType=2&weekNumber="+str(w))
        pageread = page.read()
        page.close()
        #each ESPN game ID is preceded by a squence in the html, grab all the game IDs for each week
        pagelinks = re.findall('(\d\d\d\d\d\d\d\d\d)-gameContainer', pageread)
        #for each game id picked up in previous steps, open the corresponding play by play page and extract info
        for game in pagelinks:
            #open each play by play url, copy to "gameread" and close
            gamepage = urllib.urlopen("http://scores.espn.go.com/nfl/playbyplay?gameId="+game+"&period=0")
            gameread = gamepage.read()
            gamepage.close()
            #pick up generic info on each game and save to game table
            timestamp = re.findall('<p>(\d{1,2}:\d{2}.*?20\d{2})<\/p>', gameread)
            teams = re.findall('">(\w*?)<\/a>\s*?<span id="matchup-nfl-', gameread)
            awayteam = teams[0]
            hometeam = teams[1]
            scraperwiki.sqlite.save(unique_keys=["gID"], data={"gID":gID, "espnID":game, "time":timestamp, "awayTeam":awayteam, "homeTeam":hometeam, "year":year, "week":w}, table_name="tGames2")
            tabl = re.findall('class="mod-data mod-pbp">(.*?)<\/table>', gameread) ## grab play by play table
            table = tabl[0] 
            table = table.split("<") ## delimit play by play table by html start tag
            silencer = table.pop(0) ## discard first empty cell
            i = 0
            l = len(table)
            while i < l: ## cycle through all html tagged lines and discard all but the follow 4 needed ones
                if table[i][0:2] != "h4": #indicates quarter change
                    if table[i][0:2] != "/a": #indicates possession change
                        if table[i][0:2] != "td":#all other useful info
                            if "greenfont" in table[i]:#specific format when scoring play description
                                silencer = 0
                            else:
                                silencer = table.pop(i)#the worthless ones end up here, discard them
                                i -= 1
                i += 1
                l = len(table)#for loop kind of tricky since the size and position of the loop changes within the loop
            quarter = 1
            homescore = 0
            awayscore = 0
            i = 10 ##start at 10 to avoid confusion caused by opening kickoff (before possession established)
            while i <l:#cycle through each html tagged line that was not discarded in previous step
                #establish what type of info is in the current line (4 categories)
                downdistsearch = re.search(r'width.*?px">([1-4]).*?and (\d{1,2}) at (.*)', table[i])
                score = re.search(r'td.*?"bi">(\d\d?)', table[i])
                descriptsearch = re.search("td>([\w\',().\s-]+)", table[i])
                scorech = re.search(r'greenfont', table[i])
                #additionally may be quarter change header, test that first
                if table[i][0:2] == "h4":
                    quarter = table[i][3]
                #additionally may be possession change header, test that next
                elif table[i][0:2] == "/a":
                    possession = re.search('(\w*?) at', table[i])
                elif score:
                      #if it is a score number column, do not add until you are at the home column, store away column here, and move the flag to 1, if flag is#1, then you must be at the homescore column (you just moved it to 1 in the away score column). Save the information for this scoring play and move the flag back to 1
                    if flag == 2:
                        awayscore = score.group(1)
                        flag = 1
                    elif flag == 1:
                        homescore = score.group(1)
                        flag = 0
                        scraperwiki.sqlite.save(unique_keys=["playID"], data = {"playID":playid, "quarter":quarter, "possession":possession.group(1), "down":down, "dist":dist, "spot":spot, "description":description, "awayScore":awayscore, "homeScore":homescore, "gameID":gID}, table_name="tPlay")
                        playid +=1
                elif downdistsearch:
                    #if it is a down a distance column, store those variables
                    down = downdistsearch.group(1)
                    dist = downdistsearch.group(2)
                    spot = downdistsearch.group(3)
                elif descriptsearch:
                    #if it is a description column, store that information and save
                    description = descriptsearch.group(1)
                    scraperwiki.sqlite.save(unique_keys=["playID"], data={"playID":playid, "quarter":quarter, "possession":possession.group(1), "down":down, "dist":dist, "spot":spot, "description":description, "awayScore":awayscore, "homeScore":homescore, "gameID":gID}, table_name="tPlay")
                    playid += 1
                elif scorech:
                    #if it is a scoring play description column, record the play description and move the flag to 2 (it will be saved when you get to the score columns)
                    descriptionsearch = re.search('greenfont">(.+)', table[i])
                    description = descriptionsearch.group(1)
                    flag = 2
                else:
                    silencer = 0
                i += 1
            gID +=1
        w += 1
    year += 1
