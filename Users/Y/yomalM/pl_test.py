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
            record['A- Kickoff Time'] = table_cells[0].text
            record['B- Home Team'] = table_cells[1].text
            record['C- Result'] = table_cells[2].text
            record['D- Away Team'] = table_cells[3].text
            #record['D- Rate Players'] = table_cells[3].text
           # print record, '------------'
            scraperwiki.datastore.save(["A- Kickoff Time"], record)
