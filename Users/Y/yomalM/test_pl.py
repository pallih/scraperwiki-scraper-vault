############
#Note from creator(Yomal Mudalige)- I have been tried to change column orders,  however still it is not finalized. Hence I added prefix 'A',  'B'.etc. Thanks
#Reference - Scraperwiki Tutorial 3
##################

import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Premier League Football 2011/2011 Points Tables"

html = scraperwiki.scrape('http://www.guardian.co.uk/football/premierleague/results')
soup = BeautifulSoup(html)
scraperwiki.metadata.save('data_columns', ['Kickoff time', 'Home team', 'Score line' , 'Away team'])
data_table = soup.find("table", { "class" : "team-matches first" })
rows = data_table.findAll("tr")
m = 0
for row in rows:
    print m,row
    if m < 0:
        m = m + 1
        continue
    else:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['Kickoff Time'] = table_cells[0].text
            record['Home Team'] = table_cells[1].text
            record['Result'] = table_cells[2].text
            record['Away Team'] = table_cells[3].text
            #record['D- Rate Players'] = table_cells[3].text
           # print record, '------------'
            scraperwiki.datastore.save(["Kickoff Time"], record)
############
#Note from creator(Yomal Mudalige)- I have been tried to change column orders,  however still it is not finalized. Hence I added prefix 'A',  'B'.etc. Thanks
#Reference - Scraperwiki Tutorial 3
##################

import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Premier League Football 2011/2011 Points Tables"

html = scraperwiki.scrape('http://www.guardian.co.uk/football/premierleague/results')
soup = BeautifulSoup(html)
scraperwiki.metadata.save('data_columns', ['Kickoff time', 'Home team', 'Score line' , 'Away team'])
data_table = soup.find("table", { "class" : "team-matches first" })
rows = data_table.findAll("tr")
m = 0
for row in rows:
    print m,row
    if m < 0:
        m = m + 1
        continue
    else:
        record = {}
        table_cells = row.findAll("td")
        if table_cells:
            record['Kickoff Time'] = table_cells[0].text
            record['Home Team'] = table_cells[1].text
            record['Result'] = table_cells[2].text
            record['Away Team'] = table_cells[3].text
            #record['D- Rate Players'] = table_cells[3].text
           # print record, '------------'
            scraperwiki.datastore.save(["Kickoff Time"], record)
