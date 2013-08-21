import scraperwiki
import urllib2
from lxml import etree 

url = urllib2.urlopen("http://www.output.regiosports.at/sportsml/910054-eh_20120124224203-1-98-sportsml.xml")

tree = etree.parse(url)
root = tree.getroot()
event = root[3][0][0]
dataList = []

counter = 0
for child in event:
    team1 = event[counter+1][1][0][0].attrib["full"]
    team2 = event[counter+1][2][0][0].attrib["full"]
    team1Score = event[counter+1][1][1].attrib["score"]
    team2Score = event[counter+1][2][1].attrib["score"]
    
    site = None #event[counter-1][0][1][0].tag
    
    result = team1 + " - " + team2 + " " +  team1Score + " - " + team2Score
    if team1Score > team2Score:
        winner = team1
    elif team2Score > team1Score:
        winner = team2
    else:
        winner = "equal"
        
   
    data = {'id' : counter+1,
            'team1' : team1,
            'team2' : team2,
            'winner' : winner,
            'result' : result,
            'site' : site}

    dataList.append(data)
    
    
    scraperwiki.sqlite.save(unique_keys=['id'], data=data)
    counter += 1
print dataList





