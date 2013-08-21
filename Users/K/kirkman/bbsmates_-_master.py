import scraperwiki
import mechanize
import re
import datetime
from string import Template
from BeautifulSoup import BeautifulSoup

now = datetime.datetime.now()


# this is the code to establish a schema. Only need it the first time I run.

# scraperwiki.sqlite.execute("drop table if exists `swdata`")
# scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerTeam` text, `playerNum` text, `playerStatus` text, `playerPos` text, `playerNameCode` text, `playerUrl` text, `thisSeason` text, `latestSeason` text, `playerGs` text)")



# this is the main body of the script.
# parse through list of quarterbacks, grab their names, IDs, URLs, etc, then add to a database

def scrapeBbsListingPage(theHtml):

    soup1 = BeautifulSoup(theHtml)
    
    bbs_table = soup1.find('table', {'id':'ctl00_ContentPlaceHolder1_GridView1'})

    results_pages = bbs_table.findAll('td')[0].find('table').find('tr')

    for columns in results_pages.findAll('td'):

        print(columns)



# span #ctl00_ContentPlaceHolder1_lblStatus
# Searching BBS.. Page 1 of 79




#  table#ctl00_ContentPlaceHolder1_GridView1
# tbody
# skip first two tr's
# within TR:
    #1st td has BBS name
        # within td, <a> link has format: viewbbs.aspx?id=69115
    #2nd td has sysop
    #3rd td has area code
    #4th td has members

  

#    roster_table = soup1.find('table', {'id':'result'})
    
#    for section in roster_table.findAll(re.compile('tbody'), recursive=False):
#        for row in section.findAll('tr'):
#            columns = row.findAll('td')
    
#            player_url_source = columns[2].find('a')["href"]
#            player_blob = player_url_source.replace('/player/','')
#            player_blob = player_blob.replace('/profile','')
#            player_id = player_blob.split('/')[1]
#            player_name_code = player_blob.split('/')[0]
    
#            player_url = Template("http://www.nfl.com/player/$player_name_code/$player_id/profile").substitute(player_id=player_id,player_name_code=player_name_code)
    
#            player_name_source = columns[2].find('a').text
#            player_first_name = player_name_source.split(',')[1].strip()

            

#            record = {}
#            record["playerId"] = player_id
    
            #print record
#            if record.has_key('playerId'):
                # save records to the datastore
#                scraperwiki.sqlite.save(["playerId"], record)


    # now we need to check if there are subsequent pages of players.
    # If so, then grab the URL for next page, and run the main scrapeQuarterbackPage() function again

#    resultsLinks = soup1.find('span', {'class':'linkNavigation floatRight'})
#    for link in resultsLinks.findAll('a'):
#        theLink = link.text
#        theUrl = 'http://www.nfl.com' + link.get('href')
#        print(theUrl)
#        if (theLink == 'next'):
#            html2 = scraperwiki.scrape(theUrl)
#            scrapeQuarterbackPage(html2)



# this is the code to launch the script

html1 = scraperwiki.scrape("http://bbsmates.com/browsebbs.aspx?BBSName=&AreaCode=314")

scrapeBbsListingPage(html1)

import scraperwiki
import mechanize
import re
import datetime
from string import Template
from BeautifulSoup import BeautifulSoup

now = datetime.datetime.now()


# this is the code to establish a schema. Only need it the first time I run.

# scraperwiki.sqlite.execute("drop table if exists `swdata`")
# scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerTeam` text, `playerNum` text, `playerStatus` text, `playerPos` text, `playerNameCode` text, `playerUrl` text, `thisSeason` text, `latestSeason` text, `playerGs` text)")



# this is the main body of the script.
# parse through list of quarterbacks, grab their names, IDs, URLs, etc, then add to a database

def scrapeBbsListingPage(theHtml):

    soup1 = BeautifulSoup(theHtml)
    
    bbs_table = soup1.find('table', {'id':'ctl00_ContentPlaceHolder1_GridView1'})

    results_pages = bbs_table.findAll('td')[0].find('table').find('tr')

    for columns in results_pages.findAll('td'):

        print(columns)



# span #ctl00_ContentPlaceHolder1_lblStatus
# Searching BBS.. Page 1 of 79




#  table#ctl00_ContentPlaceHolder1_GridView1
# tbody
# skip first two tr's
# within TR:
    #1st td has BBS name
        # within td, <a> link has format: viewbbs.aspx?id=69115
    #2nd td has sysop
    #3rd td has area code
    #4th td has members

  

#    roster_table = soup1.find('table', {'id':'result'})
    
#    for section in roster_table.findAll(re.compile('tbody'), recursive=False):
#        for row in section.findAll('tr'):
#            columns = row.findAll('td')
    
#            player_url_source = columns[2].find('a')["href"]
#            player_blob = player_url_source.replace('/player/','')
#            player_blob = player_blob.replace('/profile','')
#            player_id = player_blob.split('/')[1]
#            player_name_code = player_blob.split('/')[0]
    
#            player_url = Template("http://www.nfl.com/player/$player_name_code/$player_id/profile").substitute(player_id=player_id,player_name_code=player_name_code)
    
#            player_name_source = columns[2].find('a').text
#            player_first_name = player_name_source.split(',')[1].strip()

            

#            record = {}
#            record["playerId"] = player_id
    
            #print record
#            if record.has_key('playerId'):
                # save records to the datastore
#                scraperwiki.sqlite.save(["playerId"], record)


    # now we need to check if there are subsequent pages of players.
    # If so, then grab the URL for next page, and run the main scrapeQuarterbackPage() function again

#    resultsLinks = soup1.find('span', {'class':'linkNavigation floatRight'})
#    for link in resultsLinks.findAll('a'):
#        theLink = link.text
#        theUrl = 'http://www.nfl.com' + link.get('href')
#        print(theUrl)
#        if (theLink == 'next'):
#            html2 = scraperwiki.scrape(theUrl)
#            scrapeQuarterbackPage(html2)



# this is the code to launch the script

html1 = scraperwiki.scrape("http://bbsmates.com/browsebbs.aspx?BBSName=&AreaCode=314")

scrapeBbsListingPage(html1)

