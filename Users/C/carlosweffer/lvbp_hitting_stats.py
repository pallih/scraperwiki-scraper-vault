import datetime
import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

#scraperwiki.sqlite.execute('drop table if exists `swdata`')
html1 = scraperwiki.scrape("http://lvbp.com/estadisticas_gen.asp?t=bat&co_temporada=1&co_ano_temporada=6")
soup1 = BeautifulSoup(html1)

sdate = datetime.datetime.now()
sdate_split = str(sdate.year) + str(sdate.month) + str(sdate.day)
       
stats_table = soup1.find('table', {'width':'100%'}).find('table', {'width':'100%'})

#record = {}
#record['doc'] = stats_table
#scraperwiki.sqlite.save(["doc"], record)

for row in stats_table.findAll('tr'):
    record = {}
    columns = row.findAll('td')
    if columns[0].text.find('JUGADOR') < 0 :           
        record['JUGADOR'] = columns[0].text
        record['EQUIPO'] = columns[1].text
        record['AVE'] = columns[2].text
        record['JJ'] = int(columns[3].text)
        record['VB'] = int(columns[4].text)
        record['CA'] = int(columns[5].text)
        record['H'] = int(columns[6].text)
        record['BA'] = int(columns[7].text)
        record['H2'] = int(columns[8].text)
        record['H3'] = int(columns[9].text)
        record['HR'] = int(columns[10].text)
        record['CI'] = int(columns[11].text)
        record['BB'] = int(columns[12].text)
        record['SO'] = int(columns[13].text)
        record['SH'] = int(columns[14].text)
        record['SF'] = int(columns[15].text)
        record['GP'] = int(columns[16].text)
        record['BR'] = int(columns[17].text)
        record['OR'] = int(columns[18].text)
        record['SLG'] = columns[19].text
        record['OBP'] = columns[20].text
        record['FECHA'] = int(sdate_split)
        record['key'] = sdate_split + columns[1].text + columns[0].text 
        #print record
        if record.has_key('key'):
              # save records to the datastore
              scraperwiki.sqlite.save(["key"], record)

        

