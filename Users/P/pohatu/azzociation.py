import scraperwiki

# Blank Python
import urllib
import re
import sys
import lxml.html

def GetPlayersFromMinutesPage(year=2013):

    def ProcessStatsPage(url):
        players = []
        page = urllib.urlopen(url)
        pageread = page.read()
        page.close
        allrows = []
        oddrows = re.findall('oddrow(.*?)tr>', pageread)
        allrows += oddrows
        evenrows = re.findall('evenrow(.*?)tr>', pageread)
        allrows += evenrows
        for row in allrows:
            rowparts = row.split("<")
            playerID = re.findall('id\/(\d*)', rowparts[4])
            players += playerID
        print players
        nextPage = re.findall('rel="nofollow" href="(.*?)".*?-next', pageread)
        if len(nextPage) > 0:
            players += ProcessStatsPage(nextPage[0])            
        return players

    players = []
    while year < 2014:
        startPage = "http://espn.go.com/nba/statistics/player/_/stat/minutes/sort/avgMinutes/year/"+str(year)+"/qualified/false"
        players += ProcessStatsPage(startPage)
        year += 1
    return players


def ProcessPlayerPage(playerID):
        if playerID == 0: return
        playerPage = urllib.urlopen("http://espn.go.com/nba/player/_/id/"+str(playerID))
        playerPageRead = playerPage.read()
        playerPage.close
        root = lxml.html.fromstring(playerPageRead)

        playerName = ""
        pname = root.xpath('//*[@id="content"]/div[3]/div[2]/h1')
        if len(pname) == 0:
            pname = root.xpath('//*[@id="content"]/div[3]/div[1]/div[1]/h1')
        if len(pname) > 0:            
            playerName = pname[0].text

        birthDate = re.findall('(\w\w\w \d\d?, \d\d\d\d) in ', playerPageRead)
        if len(birthDate) == 0:
            birthDate = ""
        else:
            birthDate = birthDate[0]
        birthPlace = re.findall(' in (.*?) \(Age: ', playerPageRead)
        if len(birthPlace) == 0:
            birthPlace = ""
        else:
            birthPlace = birthPlace[0]
        draftYear = re.findall('(\d\d\d\d): \d.. Rnd', playerPageRead)
        if len(draftYear) == 0:
            draftYear = ""
        else:
            draftYear = draftYear[0]
        draftRound = re.findall('\d\d\d\d: (\d).. Rnd', playerPageRead)
        if len(draftRound) == 0:
            draftRound = ""
        else:
            draftRound = draftRound[0]
        draftSlot = re.findall('Rnd, (\d*?).. by ', playerPageRead)
        if len(draftSlot) == 0:
            draftSlot = ""
        else:
            draftSlot = draftSlot[0]
        college = re.findall('College</span>(.*?)</li>', playerPageRead)
        if len(college) == 0:
            college = ""
        else:
            college = college[0]
        scraperwiki.sqlite.save(unique_keys=["playerID"], data={"playerID":playerID, "playerName":playerName, "birthDate":birthDate, "birthPlace":birthPlace, "draftYear":draftYear, "draftRound":draftRound, "draftSlot":draftSlot, "college":college}, table_name="players")




players = []
players = GetPlayersFromMinutesPage(2013)
print len(players)
players = list(set(players))
print len(players)
for playerID in players:
    ProcessPlayerPage(playerID)

