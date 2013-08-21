import scraperwiki
from BeautifulSoup import BeautifulSoup

print "Premier League Football 2011/2011 Points Tables"
#-------------------------------------------------------------------------------------------
html2 = scraperwiki.scrape('http://www.guardian.co.uk/football/premierleague')
soup = BeautifulSoup(html2)
scraperwiki.metadata.save('data_columns', ['Team', 'Pld', 'GD' , 'Pts', ''])
data_table = soup.find("table", { "class" : "full" })
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
            record['A- Team'] = table_cells[0].text
            record['B-Matches Played'] = table_cells[1].text
            record['C-Goal Difference'] = table_cells[2].text
            record['D-Points'] = table_cells[3].text
          #  if table_cells[0].text = "Arsenal":
           #     record['Captain'] = "fabregas"
           # else:
            #    record['Captain'] = "test_captain"
            print record, '------------'
            scraperwiki.datastore.save(["A- Team"], record)

#--------------------------------------------------------------------------

#html1 = scraperwiki.scrape('http://www.guardian.co.uk/football/premierleague')
#soup = BeautifulSoup(html1)
#scraperwiki.metadata.save('data_columns', ['Team', 'Pld', 'GD' , 'Pts'])
#data_table = soup.find("table", { "class" : "full" })
#rows = data_table.findAll("tr")
#m = 0
#for row in rows:
 #   print m,row
 #   if m < 0:
  #      m = m + 1
   #     continue
  #  else:
    #    record = {}
     #   table_cells = row.findAll("td")
      #  if table_cells:
       #     record['e- Team'] = table_cells[0].text
        #    record['f-Matches Played'] = table_cells[1].text
         #   record['g-Goal Difference'] = table_cells[2].text
          #  record['h-Points'] = table_cells[3].text
           # print record, '------------'
            #scraperwiki.datastore.save(["e- Team"], record)



