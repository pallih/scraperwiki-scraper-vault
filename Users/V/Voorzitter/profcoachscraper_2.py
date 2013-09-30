# --[ ABOUT Profcoachscraper ]---------------------------------------------------

# This scraper has been build to retrieve data from the profcoach.nl website.
# The website provides an online soccer management game, but does not have enough
# statistical information.
# Therefore this scraper has been build.

# Constant values
# ---------------
# Values that will be used within the scraper. 
aSyst = ['4-4-3', '4-4-2', '3-4-3', '3-5-2']
dataSource = ['0149bf58-8f4e-42d4-bb8b-d14568edbd25', 'dbe59932-3ffa-4e6d-b094-00af0d9b046a', 'f748e61e-f262-4fe5-8bb1-aa6a7c395f88', '60199035-4572-49ce-8fd2-dd22f0a8bc5c', '19603b49-4810-4502-9212-61d0ca4eeed4', 'bbb44d5f-9a51-4de2-992a-0c19f2641034', '3bed87d1-1789-4a6f-99e2-0a303cce3514', 'b895bbd5-62cf-4f98-adcf-24eacd19343b', 'f87cf00d-e176-4595-b13a-9f5a98e6406d', 'e27204e7-eaad-4527-8ae3-b1d13e3811bf']

# Import libraries
import scraperwiki
import mechanize
import cookielib
import lxml.html
from lxml import etree

# Definitions
# -----------
# Generic 'functions' that will be called during the execution of the scraper.

#Retrieve the teamname form the root object
def get_teamname(root):
    h1 = root.cssselect('h1')[0].text_content().strip()
    return h1

#Get max x players within a list of players
def getmax(players, playertype, number=4):
    scores = [x['player_pntscor'] for x in players if x['player_type']==playertype]
    scores.sort()
    return sum(scores[-number:])

#Get the indexvalue of the position in the list.
def index_max(values):
    return max(xrange(len(values)),key=values.__getitem__)

# --[ START Processing ]--------------------------------------------------------
# As the data of profcoach.nl is only available after logging into the database
# we are forced to use the Mechanize library to get out the HTML so we can
# process the data.

# Browser
# -------
# Make use of Mechanize as we need to be logged on to see the data
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2')]

# Open profcoach.nl website to able to logon to eredivisie.nl
r = br.open('http://profcoach.nl/Team/0149bf58-8f4e-42d4-bb8b-d14568edbd25')

# Find the correct link to logon 'Registreren / Login'
br.find_link(text='Registreren / Login')

# Actually clicking the link
req = br.click_link(text='Registreren / Login')
br.open(req)

# Select the first (index zero) form
br.select_form(nr=0)

# User credentials - DUMMY User has been created for this!!!
br.form['email'] = 'woudloper@gmail.com'
br.form['password'] = 'dummyPCScraper'

# Login
br.submit()

# --[ MAIN Processing section ]-------------------------------------------------
# This section will loop through the teams that have been defined in the 
# 'dataSource' variable. For all those teams the data will be retrieved and put
# into the tables belonging to this scraper.
for source in dataSource:
    # Open profcoach.nl website
    r = br.open('http://profcoach.nl/Team/'+source)

    html = r.read()
    
    # Get General details
    CaptainID = html[html.find("updateCaptain('")+15:html.find("'", html.find("updateCaptain('")+15)]
    RoundInfo = html[html.find("Opstelling van ")+15:html.find("</h3>", html.find("Opstelling van ")+16)]
    
    # Read out the data
    tree = lxml.html.fromstring(html)
    
    #Read out the Teamscore
    scores = tree.cssselect('.box')
    RoundScore = int(scores[0].cssselect('span')[0].text_content().strip())
    RoundPosition = scores[1].cssselect('span')[0].text_content().strip()
    RoundTotalScore = RoundPosition = scores[1].cssselect('span')[0].text_content().strip()
    
    #Read details of the players in the soccer team
    players = tree.cssselect('.player')
    for player in players:
        data = {
            'player_id' : player.get('personid'),
            'player_name' : player.cssselect('.name')[0].get('title'),
            'player_points' : int(player.cssselect('.team')[0].text_content().strip()),
            'player_pntscor' : ((int(player.cssselect('.team')[0].text_content().strip())/2) if player.get('personid') == CaptainID else int(player.cssselect('.team')[0].text_content().strip())),
            'player_position' : ('Bankspeler' if player.get('slot') is None else 'Basisspeler'),
            'player_type' : ('Aanvaller' if player.get('class') == 'player pos4' else ('Middenvelder' if player.get('class') == 'player pos3' else ('Verdediger' if player.get('class') == 'player pos2' else 'Keeper'))),
            'player_captain' : ('Ja' if player.get('personid') == CaptainID else 'Nee'),
            'player_team' : get_teamname(tree),
            'player_teamid' : source, 
            'player_round' : RoundInfo
        }

        #Store the retrieve data in this loop/iteration to the database
        scraperwiki.sqlite.save(unique_keys=['player_team', 'player_round', 'player_id'], data=data, table_name="pcteamplayers")

    #Query above data to get extra details for the team information
    rawbench = scraperwiki.sqlite.select("sum(player_pntscor) as bnchscore from pcteamplayers where player_teamid = '" + source + "' and player_round='" + RoundInfo + "' and player_position='Bankspeler'" )
    rawplayers = scraperwiki.sqlite.select("* from pcteamplayers where player_teamid = '" + source + "' and player_round='" + RoundInfo + "'" )
    rawbestplayer = scraperwiki.sqlite.select("max(player_pntscor) as best from pcteamplayers where player_teamid = ?",source)
    #Make calculation for the best team and system used
    i443 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 4)+getmax(rawplayers, 'Middenvelder', 3)+getmax(rawplayers, 'Aanvaller', 3))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    i442 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 4)+getmax(rawplayers, 'Middenvelder', 4)+getmax(rawplayers, 'Aanvaller', 2))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    i343 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 3)+getmax(rawplayers, 'Middenvelder', 4)+getmax(rawplayers, 'Aanvaller', 3))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    i352 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 3)+getmax(rawplayers, 'Middenvelder', 5)+getmax(rawplayers, 'Aanvaller', 2))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))

    #Calculate the best team and get the corresponding system from the list
    sMaxScore = max((i443), (i442), (i343), (i352))
    sBstSyst = aSyst[index_max([i443, i442, i343, i352])]

    # Now single datastore for the team information
    scraperwiki.sqlite.save(unique_keys=["team_name", "team_round"], data={"team_id": source, "team_name":get_teamname(tree), "team_round":RoundInfo, "team_roundscore":RoundScore, "team_totalscore": RoundTotalScore, "team_roundposition":RoundPosition, "team_benchscore": rawbench[0]['bnchscore'] ,"team_maxscore":sMaxScore, "team_bestsystem":sBstSyst}, table_name = "pcteams")



# --[ ABOUT Profcoachscraper ]---------------------------------------------------

# This scraper has been build to retrieve data from the profcoach.nl website.
# The website provides an online soccer management game, but does not have enough
# statistical information.
# Therefore this scraper has been build.

# Constant values
# ---------------
# Values that will be used within the scraper. 
aSyst = ['4-4-3', '4-4-2', '3-4-3', '3-5-2']
dataSource = ['0149bf58-8f4e-42d4-bb8b-d14568edbd25', 'dbe59932-3ffa-4e6d-b094-00af0d9b046a', 'f748e61e-f262-4fe5-8bb1-aa6a7c395f88', '60199035-4572-49ce-8fd2-dd22f0a8bc5c', '19603b49-4810-4502-9212-61d0ca4eeed4', 'bbb44d5f-9a51-4de2-992a-0c19f2641034', '3bed87d1-1789-4a6f-99e2-0a303cce3514', 'b895bbd5-62cf-4f98-adcf-24eacd19343b', 'f87cf00d-e176-4595-b13a-9f5a98e6406d', 'e27204e7-eaad-4527-8ae3-b1d13e3811bf']

# Import libraries
import scraperwiki
import mechanize
import cookielib
import lxml.html
from lxml import etree

# Definitions
# -----------
# Generic 'functions' that will be called during the execution of the scraper.

#Retrieve the teamname form the root object
def get_teamname(root):
    h1 = root.cssselect('h1')[0].text_content().strip()
    return h1

#Get max x players within a list of players
def getmax(players, playertype, number=4):
    scores = [x['player_pntscor'] for x in players if x['player_type']==playertype]
    scores.sort()
    return sum(scores[-number:])

#Get the indexvalue of the position in the list.
def index_max(values):
    return max(xrange(len(values)),key=values.__getitem__)

# --[ START Processing ]--------------------------------------------------------
# As the data of profcoach.nl is only available after logging into the database
# we are forced to use the Mechanize library to get out the HTML so we can
# process the data.

# Browser
# -------
# Make use of Mechanize as we need to be logged on to see the data
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

# User-Agent (this is cheating, ok?)
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2')]

# Open profcoach.nl website to able to logon to eredivisie.nl
r = br.open('http://profcoach.nl/Team/0149bf58-8f4e-42d4-bb8b-d14568edbd25')

# Find the correct link to logon 'Registreren / Login'
br.find_link(text='Registreren / Login')

# Actually clicking the link
req = br.click_link(text='Registreren / Login')
br.open(req)

# Select the first (index zero) form
br.select_form(nr=0)

# User credentials - DUMMY User has been created for this!!!
br.form['email'] = 'woudloper@gmail.com'
br.form['password'] = 'dummyPCScraper'

# Login
br.submit()

# --[ MAIN Processing section ]-------------------------------------------------
# This section will loop through the teams that have been defined in the 
# 'dataSource' variable. For all those teams the data will be retrieved and put
# into the tables belonging to this scraper.
for source in dataSource:
    # Open profcoach.nl website
    r = br.open('http://profcoach.nl/Team/'+source)

    html = r.read()
    
    # Get General details
    CaptainID = html[html.find("updateCaptain('")+15:html.find("'", html.find("updateCaptain('")+15)]
    RoundInfo = html[html.find("Opstelling van ")+15:html.find("</h3>", html.find("Opstelling van ")+16)]
    
    # Read out the data
    tree = lxml.html.fromstring(html)
    
    #Read out the Teamscore
    scores = tree.cssselect('.box')
    RoundScore = int(scores[0].cssselect('span')[0].text_content().strip())
    RoundPosition = scores[1].cssselect('span')[0].text_content().strip()
    RoundTotalScore = RoundPosition = scores[1].cssselect('span')[0].text_content().strip()
    
    #Read details of the players in the soccer team
    players = tree.cssselect('.player')
    for player in players:
        data = {
            'player_id' : player.get('personid'),
            'player_name' : player.cssselect('.name')[0].get('title'),
            'player_points' : int(player.cssselect('.team')[0].text_content().strip()),
            'player_pntscor' : ((int(player.cssselect('.team')[0].text_content().strip())/2) if player.get('personid') == CaptainID else int(player.cssselect('.team')[0].text_content().strip())),
            'player_position' : ('Bankspeler' if player.get('slot') is None else 'Basisspeler'),
            'player_type' : ('Aanvaller' if player.get('class') == 'player pos4' else ('Middenvelder' if player.get('class') == 'player pos3' else ('Verdediger' if player.get('class') == 'player pos2' else 'Keeper'))),
            'player_captain' : ('Ja' if player.get('personid') == CaptainID else 'Nee'),
            'player_team' : get_teamname(tree),
            'player_teamid' : source, 
            'player_round' : RoundInfo
        }

        #Store the retrieve data in this loop/iteration to the database
        scraperwiki.sqlite.save(unique_keys=['player_team', 'player_round', 'player_id'], data=data, table_name="pcteamplayers")

    #Query above data to get extra details for the team information
    rawbench = scraperwiki.sqlite.select("sum(player_pntscor) as bnchscore from pcteamplayers where player_teamid = '" + source + "' and player_round='" + RoundInfo + "' and player_position='Bankspeler'" )
    rawplayers = scraperwiki.sqlite.select("* from pcteamplayers where player_teamid = '" + source + "' and player_round='" + RoundInfo + "'" )
    rawbestplayer = scraperwiki.sqlite.select("max(player_pntscor) as best from pcteamplayers where player_teamid = ?",source)
    #Make calculation for the best team and system used
    i443 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 4)+getmax(rawplayers, 'Middenvelder', 3)+getmax(rawplayers, 'Aanvaller', 3))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    i442 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 4)+getmax(rawplayers, 'Middenvelder', 4)+getmax(rawplayers, 'Aanvaller', 2))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    i343 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 3)+getmax(rawplayers, 'Middenvelder', 4)+getmax(rawplayers, 'Aanvaller', 3))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))
    i352 = (((getmax(rawplayers, 'Keeper', 1)+getmax(rawplayers, 'Verdediger', 3)+getmax(rawplayers, 'Middenvelder', 5)+getmax(rawplayers, 'Aanvaller', 2))-rawbestplayer[0]['best'])+(2*rawbestplayer[0]['best']))

    #Calculate the best team and get the corresponding system from the list
    sMaxScore = max((i443), (i442), (i343), (i352))
    sBstSyst = aSyst[index_max([i443, i442, i343, i352])]

    # Now single datastore for the team information
    scraperwiki.sqlite.save(unique_keys=["team_name", "team_round"], data={"team_id": source, "team_name":get_teamname(tree), "team_round":RoundInfo, "team_roundscore":RoundScore, "team_totalscore": RoundTotalScore, "team_roundposition":RoundPosition, "team_benchscore": rawbench[0]['bnchscore'] ,"team_maxscore":sMaxScore, "team_bestsystem":sBstSyst}, table_name = "pcteams")



