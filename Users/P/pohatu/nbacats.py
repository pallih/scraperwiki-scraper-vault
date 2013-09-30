# Blank Python
sourcescraper = ''
import urllib
import lxml.html

UANBA = ["Jason Terry", "Richard Jefferson", "Luke Walton", "Chase Budinger", "Andre Iguodala", "Jerryd Bayless", "Derrick Williams"]

htmlout=""

for player in UANBA:
    pu = player.lower().replace(' ','_')
    page = urllib.urlopen("http://www.nba.com/playerfile/"+pu+"/")
    pageread = page.read()
    page.close
    root = lxml.html.fromstring(pageread)
    last3gameshtml = root.xpath('//*[@id="mainColPlayers"]/div/div[2]')
    htmlout += "<H1>"+player+"</H1>"
    htmlout += lxml.html.tostring(last3gameshtml[0])
    htmlout += "<BR>"


print htmlout
# Blank Python
sourcescraper = ''
import urllib
import lxml.html

UANBA = ["Jason Terry", "Richard Jefferson", "Luke Walton", "Chase Budinger", "Andre Iguodala", "Jerryd Bayless", "Derrick Williams"]

htmlout=""

for player in UANBA:
    pu = player.lower().replace(' ','_')
    page = urllib.urlopen("http://www.nba.com/playerfile/"+pu+"/")
    pageread = page.read()
    page.close
    root = lxml.html.fromstring(pageread)
    last3gameshtml = root.xpath('//*[@id="mainColPlayers"]/div/div[2]')
    htmlout += "<H1>"+player+"</H1>"
    htmlout += lxml.html.tostring(last3gameshtml[0])
    htmlout += "<BR>"


print htmlout
