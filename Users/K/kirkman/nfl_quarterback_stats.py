import scraperwiki
import re
import datetime
from string import Template
from BeautifulSoup import BeautifulSoup

now = datetime.datetime.now()


# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerTeam` text, `playerNum` text, `playerStatus` text, `playerPos` text, `playerNameCode` text, `playerUrl` text, `thisSeason` text, `latestSeason` text, `playerGs` text)")



# this is the main body of the script.
# parse through list of quarterbacks, grab their names, IDs, URLs, etc, then add to a database

def scrapeQuarterbackPage(theHtml):

    soup1 = BeautifulSoup(theHtml)
    
    roster_table = soup1.find('table', {'id':'result'})
    
    for section in roster_table.findAll(re.compile('tbody'), recursive=False):
        for row in section.findAll('tr'):
            columns = row.findAll('td')
    
            player_url_source = columns[2].find('a')["href"]
            player_blob = player_url_source.replace('/player/','')
            player_blob = player_blob.replace('/profile','')
            player_id = player_blob.split('/')[1]
            player_name_code = player_blob.split('/')[0]
    
            player_url = Template("http://www.nfl.com/player/$player_name_code/$player_id/profile").substitute(player_id=player_id,player_name_code=player_name_code)
    
            player_name_source = columns[2].find('a').text
            player_first_name = player_name_source.split(',')[1].strip()
            player_last_name = player_name_source.split(',')[0].strip()
            player_full_name = player_first_name + ' ' + player_last_name
            player_position = columns[0].text
            player_team = columns[12].find('a').text
            player_uni_number = columns[1].text
            player_status = columns[3].text
        

            # now lets go to his stats page and capture Games Started information

            html2 = scraperwiki.scrape(player_url)
            soup2 = BeautifulSoup(html2)
    
            player_stat_wrapper = soup2.find('div', {'id':'player-stats-wrapper'})

            # These stat tables do not have unique IDs. The first one is Recent Games,
            # the second one is Career Stats. I want the second one, so grab 2nd in the array
            career_stats_table = player_stat_wrapper.findAll('table')[1]

            # there's no TBODY tag, so get all TRs and skip down to the fourth one, 
            # which will be the most recent season

            career_stats_rows = career_stats_table.findAll('tr')

            # check to make sure there's no colspan, which is the case if a player has NO career stats
            if (not career_stats_rows[1].td.has_key('colspan')): 

                my_row = career_stats_rows[3]
                my_columns = my_row.findAll('td')

                latest_season = int(my_columns[0].text)
                this_season = now.year

                # make sure the column doesn't have dashes
                if (my_columns[3].text != '--'):
                    player_Gs = my_columns[3].text

                # If it does have dashes, record zero instead
                else:
                    player_Gs = 0

            # so, this player has NO career stats
            else:
                latest_season = ''
                this_season = now.year
                myGs = 0
            

            record = {}
            record["playerId"] = player_id
            record["playerFullName"] = player_full_name
            record["playerFirstName"] = player_first_name
            record["playerLastName"] = player_last_name
            record["playerNameCode"] = player_name_code
            record["playerStatus"] = player_status
            record["playerUrl"] = player_url
            record["playerTeam"] = player_team
            record["playerPos"] = player_position
            record["playerNum"] = player_uni_number
            record["thisSeason"] = this_season
            record["latestSeason"] = latest_season
            record["playerGs"] = player_Gs
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(["playerId"], record)


    # now we need to check if there are subsequent pages of players.
    # If so, then grab the URL for next page, and run the main scrapeQuarterbackPage() function again

    resultsLinks = soup1.find('span', {'class':'linkNavigation floatRight'})
    for link in resultsLinks.findAll('a'):
        theLink = link.text
        theUrl = 'http://www.nfl.com' + link.get('href')
        print(theUrl)
        if (theLink == 'next'):
            html2 = scraperwiki.scrape(theUrl)
            scrapeQuarterbackPage(html2)



# this is the code to launch the script

html1 = scraperwiki.scrape("http://www.nfl.com/players/search?category=position&filter=quarterback&conferenceAbbr=null&playerType=current&conference=ALL")

scrapeQuarterbackPage(html1)

import scraperwiki
import re
import datetime
from string import Template
from BeautifulSoup import BeautifulSoup

now = datetime.datetime.now()


# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerTeam` text, `playerNum` text, `playerStatus` text, `playerPos` text, `playerNameCode` text, `playerUrl` text, `thisSeason` text, `latestSeason` text, `playerGs` text)")



# this is the main body of the script.
# parse through list of quarterbacks, grab their names, IDs, URLs, etc, then add to a database

def scrapeQuarterbackPage(theHtml):

    soup1 = BeautifulSoup(theHtml)
    
    roster_table = soup1.find('table', {'id':'result'})
    
    for section in roster_table.findAll(re.compile('tbody'), recursive=False):
        for row in section.findAll('tr'):
            columns = row.findAll('td')
    
            player_url_source = columns[2].find('a')["href"]
            player_blob = player_url_source.replace('/player/','')
            player_blob = player_blob.replace('/profile','')
            player_id = player_blob.split('/')[1]
            player_name_code = player_blob.split('/')[0]
    
            player_url = Template("http://www.nfl.com/player/$player_name_code/$player_id/profile").substitute(player_id=player_id,player_name_code=player_name_code)
    
            player_name_source = columns[2].find('a').text
            player_first_name = player_name_source.split(',')[1].strip()
            player_last_name = player_name_source.split(',')[0].strip()
            player_full_name = player_first_name + ' ' + player_last_name
            player_position = columns[0].text
            player_team = columns[12].find('a').text
            player_uni_number = columns[1].text
            player_status = columns[3].text
        

            # now lets go to his stats page and capture Games Started information

            html2 = scraperwiki.scrape(player_url)
            soup2 = BeautifulSoup(html2)
    
            player_stat_wrapper = soup2.find('div', {'id':'player-stats-wrapper'})

            # These stat tables do not have unique IDs. The first one is Recent Games,
            # the second one is Career Stats. I want the second one, so grab 2nd in the array
            career_stats_table = player_stat_wrapper.findAll('table')[1]

            # there's no TBODY tag, so get all TRs and skip down to the fourth one, 
            # which will be the most recent season

            career_stats_rows = career_stats_table.findAll('tr')

            # check to make sure there's no colspan, which is the case if a player has NO career stats
            if (not career_stats_rows[1].td.has_key('colspan')): 

                my_row = career_stats_rows[3]
                my_columns = my_row.findAll('td')

                latest_season = int(my_columns[0].text)
                this_season = now.year

                # make sure the column doesn't have dashes
                if (my_columns[3].text != '--'):
                    player_Gs = my_columns[3].text

                # If it does have dashes, record zero instead
                else:
                    player_Gs = 0

            # so, this player has NO career stats
            else:
                latest_season = ''
                this_season = now.year
                myGs = 0
            

            record = {}
            record["playerId"] = player_id
            record["playerFullName"] = player_full_name
            record["playerFirstName"] = player_first_name
            record["playerLastName"] = player_last_name
            record["playerNameCode"] = player_name_code
            record["playerStatus"] = player_status
            record["playerUrl"] = player_url
            record["playerTeam"] = player_team
            record["playerPos"] = player_position
            record["playerNum"] = player_uni_number
            record["thisSeason"] = this_season
            record["latestSeason"] = latest_season
            record["playerGs"] = player_Gs
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(["playerId"], record)


    # now we need to check if there are subsequent pages of players.
    # If so, then grab the URL for next page, and run the main scrapeQuarterbackPage() function again

    resultsLinks = soup1.find('span', {'class':'linkNavigation floatRight'})
    for link in resultsLinks.findAll('a'):
        theLink = link.text
        theUrl = 'http://www.nfl.com' + link.get('href')
        print(theUrl)
        if (theLink == 'next'):
            html2 = scraperwiki.scrape(theUrl)
            scrapeQuarterbackPage(html2)



# this is the code to launch the script

html1 = scraperwiki.scrape("http://www.nfl.com/players/search?category=position&filter=quarterback&conferenceAbbr=null&playerType=current&conference=ALL")

scrapeQuarterbackPage(html1)

import scraperwiki
import re
import datetime
from string import Template
from BeautifulSoup import BeautifulSoup

now = datetime.datetime.now()


# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerTeam` text, `playerNum` text, `playerStatus` text, `playerPos` text, `playerNameCode` text, `playerUrl` text, `thisSeason` text, `latestSeason` text, `playerGs` text)")



# this is the main body of the script.
# parse through list of quarterbacks, grab their names, IDs, URLs, etc, then add to a database

def scrapeQuarterbackPage(theHtml):

    soup1 = BeautifulSoup(theHtml)
    
    roster_table = soup1.find('table', {'id':'result'})
    
    for section in roster_table.findAll(re.compile('tbody'), recursive=False):
        for row in section.findAll('tr'):
            columns = row.findAll('td')
    
            player_url_source = columns[2].find('a')["href"]
            player_blob = player_url_source.replace('/player/','')
            player_blob = player_blob.replace('/profile','')
            player_id = player_blob.split('/')[1]
            player_name_code = player_blob.split('/')[0]
    
            player_url = Template("http://www.nfl.com/player/$player_name_code/$player_id/profile").substitute(player_id=player_id,player_name_code=player_name_code)
    
            player_name_source = columns[2].find('a').text
            player_first_name = player_name_source.split(',')[1].strip()
            player_last_name = player_name_source.split(',')[0].strip()
            player_full_name = player_first_name + ' ' + player_last_name
            player_position = columns[0].text
            player_team = columns[12].find('a').text
            player_uni_number = columns[1].text
            player_status = columns[3].text
        

            # now lets go to his stats page and capture Games Started information

            html2 = scraperwiki.scrape(player_url)
            soup2 = BeautifulSoup(html2)
    
            player_stat_wrapper = soup2.find('div', {'id':'player-stats-wrapper'})

            # These stat tables do not have unique IDs. The first one is Recent Games,
            # the second one is Career Stats. I want the second one, so grab 2nd in the array
            career_stats_table = player_stat_wrapper.findAll('table')[1]

            # there's no TBODY tag, so get all TRs and skip down to the fourth one, 
            # which will be the most recent season

            career_stats_rows = career_stats_table.findAll('tr')

            # check to make sure there's no colspan, which is the case if a player has NO career stats
            if (not career_stats_rows[1].td.has_key('colspan')): 

                my_row = career_stats_rows[3]
                my_columns = my_row.findAll('td')

                latest_season = int(my_columns[0].text)
                this_season = now.year

                # make sure the column doesn't have dashes
                if (my_columns[3].text != '--'):
                    player_Gs = my_columns[3].text

                # If it does have dashes, record zero instead
                else:
                    player_Gs = 0

            # so, this player has NO career stats
            else:
                latest_season = ''
                this_season = now.year
                myGs = 0
            

            record = {}
            record["playerId"] = player_id
            record["playerFullName"] = player_full_name
            record["playerFirstName"] = player_first_name
            record["playerLastName"] = player_last_name
            record["playerNameCode"] = player_name_code
            record["playerStatus"] = player_status
            record["playerUrl"] = player_url
            record["playerTeam"] = player_team
            record["playerPos"] = player_position
            record["playerNum"] = player_uni_number
            record["thisSeason"] = this_season
            record["latestSeason"] = latest_season
            record["playerGs"] = player_Gs
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(["playerId"], record)


    # now we need to check if there are subsequent pages of players.
    # If so, then grab the URL for next page, and run the main scrapeQuarterbackPage() function again

    resultsLinks = soup1.find('span', {'class':'linkNavigation floatRight'})
    for link in resultsLinks.findAll('a'):
        theLink = link.text
        theUrl = 'http://www.nfl.com' + link.get('href')
        print(theUrl)
        if (theLink == 'next'):
            html2 = scraperwiki.scrape(theUrl)
            scrapeQuarterbackPage(html2)



# this is the code to launch the script

html1 = scraperwiki.scrape("http://www.nfl.com/players/search?category=position&filter=quarterback&conferenceAbbr=null&playerType=current&conference=ALL")

scrapeQuarterbackPage(html1)

import scraperwiki
import re
import datetime
from string import Template
from BeautifulSoup import BeautifulSoup

now = datetime.datetime.now()


# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerTeam` text, `playerNum` text, `playerStatus` text, `playerPos` text, `playerNameCode` text, `playerUrl` text, `thisSeason` text, `latestSeason` text, `playerGs` text)")



# this is the main body of the script.
# parse through list of quarterbacks, grab their names, IDs, URLs, etc, then add to a database

def scrapeQuarterbackPage(theHtml):

    soup1 = BeautifulSoup(theHtml)
    
    roster_table = soup1.find('table', {'id':'result'})
    
    for section in roster_table.findAll(re.compile('tbody'), recursive=False):
        for row in section.findAll('tr'):
            columns = row.findAll('td')
    
            player_url_source = columns[2].find('a')["href"]
            player_blob = player_url_source.replace('/player/','')
            player_blob = player_blob.replace('/profile','')
            player_id = player_blob.split('/')[1]
            player_name_code = player_blob.split('/')[0]
    
            player_url = Template("http://www.nfl.com/player/$player_name_code/$player_id/profile").substitute(player_id=player_id,player_name_code=player_name_code)
    
            player_name_source = columns[2].find('a').text
            player_first_name = player_name_source.split(',')[1].strip()
            player_last_name = player_name_source.split(',')[0].strip()
            player_full_name = player_first_name + ' ' + player_last_name
            player_position = columns[0].text
            player_team = columns[12].find('a').text
            player_uni_number = columns[1].text
            player_status = columns[3].text
        

            # now lets go to his stats page and capture Games Started information

            html2 = scraperwiki.scrape(player_url)
            soup2 = BeautifulSoup(html2)
    
            player_stat_wrapper = soup2.find('div', {'id':'player-stats-wrapper'})

            # These stat tables do not have unique IDs. The first one is Recent Games,
            # the second one is Career Stats. I want the second one, so grab 2nd in the array
            career_stats_table = player_stat_wrapper.findAll('table')[1]

            # there's no TBODY tag, so get all TRs and skip down to the fourth one, 
            # which will be the most recent season

            career_stats_rows = career_stats_table.findAll('tr')

            # check to make sure there's no colspan, which is the case if a player has NO career stats
            if (not career_stats_rows[1].td.has_key('colspan')): 

                my_row = career_stats_rows[3]
                my_columns = my_row.findAll('td')

                latest_season = int(my_columns[0].text)
                this_season = now.year

                # make sure the column doesn't have dashes
                if (my_columns[3].text != '--'):
                    player_Gs = my_columns[3].text

                # If it does have dashes, record zero instead
                else:
                    player_Gs = 0

            # so, this player has NO career stats
            else:
                latest_season = ''
                this_season = now.year
                myGs = 0
            

            record = {}
            record["playerId"] = player_id
            record["playerFullName"] = player_full_name
            record["playerFirstName"] = player_first_name
            record["playerLastName"] = player_last_name
            record["playerNameCode"] = player_name_code
            record["playerStatus"] = player_status
            record["playerUrl"] = player_url
            record["playerTeam"] = player_team
            record["playerPos"] = player_position
            record["playerNum"] = player_uni_number
            record["thisSeason"] = this_season
            record["latestSeason"] = latest_season
            record["playerGs"] = player_Gs
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(["playerId"], record)


    # now we need to check if there are subsequent pages of players.
    # If so, then grab the URL for next page, and run the main scrapeQuarterbackPage() function again

    resultsLinks = soup1.find('span', {'class':'linkNavigation floatRight'})
    for link in resultsLinks.findAll('a'):
        theLink = link.text
        theUrl = 'http://www.nfl.com' + link.get('href')
        print(theUrl)
        if (theLink == 'next'):
            html2 = scraperwiki.scrape(theUrl)
            scrapeQuarterbackPage(html2)



# this is the code to launch the script

html1 = scraperwiki.scrape("http://www.nfl.com/players/search?category=position&filter=quarterback&conferenceAbbr=null&playerType=current&conference=ALL")

scrapeQuarterbackPage(html1)

