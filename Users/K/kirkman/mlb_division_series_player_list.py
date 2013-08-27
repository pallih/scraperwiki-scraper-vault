import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup


# this is the main body of the script.
# parse through a team's roster list, grab their names, IDs, URLs, etc, then add to a database

def scrapeRosterPage(theHtml,team_id):

    soup2 = BeautifulSoup(theHtml)
    
    roster_div = soup2.find(id='mc')

    roster_table = roster_div.find('table')
    

    for section in roster_table.findAll(re.compile('tbody'), recursive=False):
        for row in section.findAll('tr'):
            columns = row.findAll('td')
    
            player_position = section.findPrevious('thead').find('tr').findAll('th')[1].text
            if player_position == 'Pitchers':
                player_position = 'P'
            elif player_position == 'Catchers':
                player_position = 'C'
            elif player_position == 'Infielders':
                player_position = 'IF'
            elif player_position == 'Outfielders':
                player_position = 'OF'

            #  /team/player.jsp?player_id=459939
            player_url_source = columns[1].find('a')["href"]
            player_id = player_url_source.split('=')[1]
    
            player_url = Template("http://mlb.mlb.com/team/player.jsp?player_id=$player_id").substitute(player_id=player_id)
    
            player_name_source = columns[1].find('a').text
            player_name = player_name_source.replace('/\*/','')
            player_name = player_name_source.replace('/\#/','')

            player_first_name = player_name_source.split(' ')[0].strip()
            player_last_name = player_name_source.split(' ')[1].strip()
            player_full_name = player_first_name + ' ' + player_last_name

            player_uni = columns[0].text

            if team_id == 'bal':
                team_name = 'Orioles'
            elif team_id == 'tex':
                team_name = 'Rangers'
            elif team_id == 'atl':
                team_name = 'Braves'
            elif team_id == 'stl':
                team_name = 'Cardinals'
            elif team_id == 'nyy':
                team_name = 'Yankees'
            elif team_id == 'oak':
                team_name = 'Athletics'
            elif team_id == 'det':
                team_name = 'Tigers'
            elif team_id == 'was':
                team_name = 'Nationals'
            elif team_id == 'cin':
                team_name = 'Reds'
            elif team_id == 'sf':
                team_name = 'Giants'

            record = {}
            record["playerId"] = player_id
            record["playerFullName"] = player_full_name
            record["playerFirstName"] = player_first_name
            record["playerLastName"] = player_last_name
            record["playerUrl"] = player_url
            record["playerTeam"] = team_name
            record["playerTeamId"] = team_id
            record["playerPos"] = player_position
            record["playerUni"] = player_uni
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(["playerId"], record)




# next steps:
# write a first scraper to go through the PLAYER SEARCH page, compiling team codes.
# http://mlb.mlb.com/mlb/players/?tcid=nav_mlb_players
# need to search <select id="ps_team">
# and then grab the value of each option in the list.

# <select  onchange="if(this.value!='')window.parent.location.href=this.options[this.selectedIndex].value">
#            <option value="">Team Rosters</option>
#            <option value="http://losangeles.angels.mlb.com/team/roster_40man.jsp?c_id=ana">Angels</option>
#            <option value="http://houston.astros.mlb.com/team/roster_40man.jsp?c_id=hou">Astros</option>
#            <option value="http://oakland.athletics.mlb.com/team/roster_40man.jsp?c_id=oak">Athletics</option>
#            <option value="http://toronto.bluejays.mlb.com/team/roster_40man.jsp?c_id=tor">Blue Jays</option>
#            <option value="http://atlanta.braves.mlb.com/team/roster_40man.jsp?c_id=atl">Braves</option>



# Make list of teams listed on the Playoff Picture bracket
def scrapePostseasonPicture(theHtml):

    soup1 = BeautifulSoup(theHtml)
    
    bracket = soup1.find('div', {'id':'bracket'})
    the_images = bracket.findAll('img')

    # loop through every team in the option list
    for image in the_images:
    
        team_url_source = image['src']

        if team_url_source != '' :
            team_part = team_url_source.split('.')[0]
            team_id = team_part.split('/')[6]

            # now that we have the team's URL, run the roster scraper and get that team's players
            team_url = Template("http://mlb.mlb.com/team/roster_active.jsp?c_id=$team_id").substitute(team_id=team_id)
            html2 = scraperwiki.scrape(team_url)
            scrapeRosterPage(html2,team_id)



# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerTeamId` text, `playerPos` text, `playerUni` text)")



# this is the code to launch the script

html1 = scraperwiki.scrape("http://mlb.mlb.com/mlb/standings/postseasonpicture.jsp")
scrapePostseasonPicture(html1)



import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup


# this is the main body of the script.
# parse through a team's roster list, grab their names, IDs, URLs, etc, then add to a database

def scrapeRosterPage(theHtml,team_id):

    soup2 = BeautifulSoup(theHtml)
    
    roster_div = soup2.find(id='mc')

    roster_table = roster_div.find('table')
    

    for section in roster_table.findAll(re.compile('tbody'), recursive=False):
        for row in section.findAll('tr'):
            columns = row.findAll('td')
    
            player_position = section.findPrevious('thead').find('tr').findAll('th')[1].text
            if player_position == 'Pitchers':
                player_position = 'P'
            elif player_position == 'Catchers':
                player_position = 'C'
            elif player_position == 'Infielders':
                player_position = 'IF'
            elif player_position == 'Outfielders':
                player_position = 'OF'

            #  /team/player.jsp?player_id=459939
            player_url_source = columns[1].find('a')["href"]
            player_id = player_url_source.split('=')[1]
    
            player_url = Template("http://mlb.mlb.com/team/player.jsp?player_id=$player_id").substitute(player_id=player_id)
    
            player_name_source = columns[1].find('a').text
            player_name = player_name_source.replace('/\*/','')
            player_name = player_name_source.replace('/\#/','')

            player_first_name = player_name_source.split(' ')[0].strip()
            player_last_name = player_name_source.split(' ')[1].strip()
            player_full_name = player_first_name + ' ' + player_last_name

            player_uni = columns[0].text

            if team_id == 'bal':
                team_name = 'Orioles'
            elif team_id == 'tex':
                team_name = 'Rangers'
            elif team_id == 'atl':
                team_name = 'Braves'
            elif team_id == 'stl':
                team_name = 'Cardinals'
            elif team_id == 'nyy':
                team_name = 'Yankees'
            elif team_id == 'oak':
                team_name = 'Athletics'
            elif team_id == 'det':
                team_name = 'Tigers'
            elif team_id == 'was':
                team_name = 'Nationals'
            elif team_id == 'cin':
                team_name = 'Reds'
            elif team_id == 'sf':
                team_name = 'Giants'

            record = {}
            record["playerId"] = player_id
            record["playerFullName"] = player_full_name
            record["playerFirstName"] = player_first_name
            record["playerLastName"] = player_last_name
            record["playerUrl"] = player_url
            record["playerTeam"] = team_name
            record["playerTeamId"] = team_id
            record["playerPos"] = player_position
            record["playerUni"] = player_uni
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(["playerId"], record)




# next steps:
# write a first scraper to go through the PLAYER SEARCH page, compiling team codes.
# http://mlb.mlb.com/mlb/players/?tcid=nav_mlb_players
# need to search <select id="ps_team">
# and then grab the value of each option in the list.

# <select  onchange="if(this.value!='')window.parent.location.href=this.options[this.selectedIndex].value">
#            <option value="">Team Rosters</option>
#            <option value="http://losangeles.angels.mlb.com/team/roster_40man.jsp?c_id=ana">Angels</option>
#            <option value="http://houston.astros.mlb.com/team/roster_40man.jsp?c_id=hou">Astros</option>
#            <option value="http://oakland.athletics.mlb.com/team/roster_40man.jsp?c_id=oak">Athletics</option>
#            <option value="http://toronto.bluejays.mlb.com/team/roster_40man.jsp?c_id=tor">Blue Jays</option>
#            <option value="http://atlanta.braves.mlb.com/team/roster_40man.jsp?c_id=atl">Braves</option>



# Make list of teams listed on the Playoff Picture bracket
def scrapePostseasonPicture(theHtml):

    soup1 = BeautifulSoup(theHtml)
    
    bracket = soup1.find('div', {'id':'bracket'})
    the_images = bracket.findAll('img')

    # loop through every team in the option list
    for image in the_images:
    
        team_url_source = image['src']

        if team_url_source != '' :
            team_part = team_url_source.split('.')[0]
            team_id = team_part.split('/')[6]

            # now that we have the team's URL, run the roster scraper and get that team's players
            team_url = Template("http://mlb.mlb.com/team/roster_active.jsp?c_id=$team_id").substitute(team_id=team_id)
            html2 = scraperwiki.scrape(team_url)
            scrapeRosterPage(html2,team_id)



# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerTeamId` text, `playerPos` text, `playerUni` text)")



# this is the code to launch the script

html1 = scraperwiki.scrape("http://mlb.mlb.com/mlb/standings/postseasonpicture.jsp")
scrapePostseasonPicture(html1)



import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup


# this is the main body of the script.
# parse through a team's roster list, grab their names, IDs, URLs, etc, then add to a database

def scrapeRosterPage(theHtml,team_id):

    soup2 = BeautifulSoup(theHtml)
    
    roster_div = soup2.find(id='mc')

    roster_table = roster_div.find('table')
    

    for section in roster_table.findAll(re.compile('tbody'), recursive=False):
        for row in section.findAll('tr'):
            columns = row.findAll('td')
    
            player_position = section.findPrevious('thead').find('tr').findAll('th')[1].text
            if player_position == 'Pitchers':
                player_position = 'P'
            elif player_position == 'Catchers':
                player_position = 'C'
            elif player_position == 'Infielders':
                player_position = 'IF'
            elif player_position == 'Outfielders':
                player_position = 'OF'

            #  /team/player.jsp?player_id=459939
            player_url_source = columns[1].find('a')["href"]
            player_id = player_url_source.split('=')[1]
    
            player_url = Template("http://mlb.mlb.com/team/player.jsp?player_id=$player_id").substitute(player_id=player_id)
    
            player_name_source = columns[1].find('a').text
            player_name = player_name_source.replace('/\*/','')
            player_name = player_name_source.replace('/\#/','')

            player_first_name = player_name_source.split(' ')[0].strip()
            player_last_name = player_name_source.split(' ')[1].strip()
            player_full_name = player_first_name + ' ' + player_last_name

            player_uni = columns[0].text

            if team_id == 'bal':
                team_name = 'Orioles'
            elif team_id == 'tex':
                team_name = 'Rangers'
            elif team_id == 'atl':
                team_name = 'Braves'
            elif team_id == 'stl':
                team_name = 'Cardinals'
            elif team_id == 'nyy':
                team_name = 'Yankees'
            elif team_id == 'oak':
                team_name = 'Athletics'
            elif team_id == 'det':
                team_name = 'Tigers'
            elif team_id == 'was':
                team_name = 'Nationals'
            elif team_id == 'cin':
                team_name = 'Reds'
            elif team_id == 'sf':
                team_name = 'Giants'

            record = {}
            record["playerId"] = player_id
            record["playerFullName"] = player_full_name
            record["playerFirstName"] = player_first_name
            record["playerLastName"] = player_last_name
            record["playerUrl"] = player_url
            record["playerTeam"] = team_name
            record["playerTeamId"] = team_id
            record["playerPos"] = player_position
            record["playerUni"] = player_uni
    
            #print record
            if record.has_key('playerId'):
                # save records to the datastore
                scraperwiki.sqlite.save(["playerId"], record)




# next steps:
# write a first scraper to go through the PLAYER SEARCH page, compiling team codes.
# http://mlb.mlb.com/mlb/players/?tcid=nav_mlb_players
# need to search <select id="ps_team">
# and then grab the value of each option in the list.

# <select  onchange="if(this.value!='')window.parent.location.href=this.options[this.selectedIndex].value">
#            <option value="">Team Rosters</option>
#            <option value="http://losangeles.angels.mlb.com/team/roster_40man.jsp?c_id=ana">Angels</option>
#            <option value="http://houston.astros.mlb.com/team/roster_40man.jsp?c_id=hou">Astros</option>
#            <option value="http://oakland.athletics.mlb.com/team/roster_40man.jsp?c_id=oak">Athletics</option>
#            <option value="http://toronto.bluejays.mlb.com/team/roster_40man.jsp?c_id=tor">Blue Jays</option>
#            <option value="http://atlanta.braves.mlb.com/team/roster_40man.jsp?c_id=atl">Braves</option>



# Make list of teams listed on the Playoff Picture bracket
def scrapePostseasonPicture(theHtml):

    soup1 = BeautifulSoup(theHtml)
    
    bracket = soup1.find('div', {'id':'bracket'})
    the_images = bracket.findAll('img')

    # loop through every team in the option list
    for image in the_images:
    
        team_url_source = image['src']

        if team_url_source != '' :
            team_part = team_url_source.split('.')[0]
            team_id = team_part.split('/')[6]

            # now that we have the team's URL, run the roster scraper and get that team's players
            team_url = Template("http://mlb.mlb.com/team/roster_active.jsp?c_id=$team_id").substitute(team_id=team_id)
            html2 = scraperwiki.scrape(team_url)
            scrapeRosterPage(html2,team_id)



# this is the code to establish a schema. Only need it the first time I run.

scraperwiki.sqlite.execute("drop table if exists `swdata`")
scraperwiki.sqlite.execute("CREATE TABLE `swdata` (`playerId` text, `playerFirstName` text, `playerLastName` text, `playerFullName` text, `playerUrl` text, `playerTeam` text, `playerTeamId` text, `playerPos` text, `playerUni` text)")



# this is the code to launch the script

html1 = scraperwiki.scrape("http://mlb.mlb.com/mlb/standings/postseasonpicture.jsp")
scrapePostseasonPicture(html1)



