import scraperwiki

# Blank Python
import urllib
import re
import sys
year = 2011
while year < 2012:
    allrows = []
    page = urllib.urlopen("http://espn.go.com/nba/statistics/player/_/stat/minutes/sort/avgMinutes/year/"+str(year)+"/qualified/false")
    pageread = page.read()
    page.close
    oddrows = re.findall('oddrow(.*?)tr>', pageread)
    allrows += oddrows
    evenrows = re.findall('evenrow(.*?)tr>', pageread)
    allrows += evenrows
    for row in allrows:
        rowparts = row.split("<")
        playerID = re.findall('id\/(\d*)', rowparts[4])
        playerID = playerID[0]
        statID = int(playerID)*100 + year - 2000
        gameCount = re.findall('td\s?>(\d*)', rowparts[9])
        gameCount = gameCount[0]
        minuteCount = re.findall('td\s?>(\d*)', rowparts[11])
        minuteCount = minuteCount[0]        
        scraperwiki.sqlite.save(unique_keys=["statID"], data={"statID":statID, "playerID":playerID, "games":gameCount, "minutes":minuteCount}, table_name="stats")
        savedPlayer = scraperwiki.sqlite.select("playerID FROM players WHERE playerID=" + playerID)
        if len(savedPlayer) > 0:
            playerPage = urllib.urlopen("http://espn.go.com/nba/player/_/id/"+playerID)
            playerPageRead = playerPage.read()
            playerPage.close
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
            savedrows = scraperwiki.sqlite.select("playerID FROM players WHERE playerID =" + playerID)
            scraperwiki.sqlite.save(unique_keys=["playerID"], data={"playerID":playerID, "birthDate":birthDate, "birthPlace":birthPlace, "draftYear":draftYear, "draftRound":draftRound, "draftSlot":draftSlot, "college":college}, table_name="players")
        else:
            silencer = 0
    nextPage = re.findall('rel="nofollow" href="(.*?)".*?-next', pageread)
    while len(nextPage) > 0:
        nextPage = nextPage[0]
        allrows = []
        page = urllib.urlopen(nextPage)
        pageread = page.read()
        page.close
        oddrows = re.findall('oddrow(.*?)tr>', pageread)
        allrows += oddrows
        evenrows = re.findall('evenrow(.*?)tr>', pageread)
        allrows += evenrows
        for row in allrows:
            rowparts = row.split("<")
            playerID = re.findall('id\/(\d*)', rowparts[4])
            playerID = playerID[0]
            statID = int(playerID)*100 + year - 2000
            gameCount = re.findall('td\s?>(\d*)', rowparts[9])
            gameCount = gameCount[0]
            minuteCount = re.findall('td\s?>(\d*)', rowparts[11])
            minuteCount = minuteCount[0]        
            scraperwiki.sqlite.save(unique_keys=["statID"], data={"statID":statID, "playerID":playerID, "games":gameCount, "minutes":minuteCount}, table_name="stats")
            scraperwiki.sqlite.save(unique_keys=["statID"], data={"statID":statID, "playerID":playerID, "games":gameCount, "minutes":minuteCount}, table_name="stats")
            savedPlayer = scraperwiki.sqlite.select("playerID FROM players WHERE playerID=" + playerID)
            if len(savedPlayer) > 0:
                playerPage = urllib.urlopen("http://espn.go.com/nba/player/_/id/"+playerID)
                playerPageRead = playerPage.read()
                playerPage.close
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
                scraperwiki.sqlite.save(unique_keys=["playerID"], data={"playerID":playerID, "birthDate":birthDate, "birthPlace":birthPlace, "draftYear":draftYear, "draftRound":draftRound, "draftSlot":draftSlot, "college":college}, table_name="players")
            else:
                silencer = 0
        nextPage = re.findall('rel="nofollow" href="(.*?)".*?-next', pageread)
    year += 1