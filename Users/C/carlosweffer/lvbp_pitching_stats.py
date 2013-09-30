import datetime
import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

sdate = datetime.datetime.now()
sdate_split = str(sdate.year) + str(sdate.month) + str(sdate.day)

#scraperwiki.sqlite.execute('drop table if exists `swdata`')
html1 = scraperwiki.scrape("http://lvbp.com/estadisticas_gen.asp?t=lanz&tipo=s&co_temporada=1&co_ano_temporada=6")
soup1 = BeautifulSoup(html1)
       
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
        record['JJ'] = int(columns[2].text)
        record['JI'] = int(columns[3].text)
        record['JG'] = int(columns[4].text)
        record['JP'] = int(columns[5].text)
        record['PCT'] = columns[6].text
        record['JS'] = int(columns[7].text)
        record['JC'] = int(columns[8].text)
        record['JB'] = int(columns[9].text)
        ip_split = columns[10].text.split('.')
        record['IP'] = int(ip_split[0]) + (int(ip_split[1]) * 0.1)
        record['H'] = int(columns[11].text)
        record['H2'] = int(columns[12].text)
        record['H3'] = int(columns[13].text)
        record['HR'] = int(columns[14].text)
        record['CP'] = int(columns[15].text)
        record['CL'] = int(columns[16].text)
        record['BB'] = int(columns[17].text)
        record['SO'] = int(columns[18].text)
        record['GP'] = int(columns[19].text)
        record['WP'] = int(columns[20].text)
        record['BK'] = int(columns[21].text)
        efe_split = columns[22].text.split('.')
        record['EFE'] = int(efe_split[0]) + (int(efe_split[1]) * 0.1)
        record['FECHA'] = int(sdate_split)
        record['key'] = sdate_split + columns[1].text + columns[0].text
        #print record
        if record.has_key('key'):
              # save records to the datastore
              scraperwiki.sqlite.save(["key"], record)



import datetime
import scraperwiki
import re
from string import Template
from BeautifulSoup import BeautifulSoup

sdate = datetime.datetime.now()
sdate_split = str(sdate.year) + str(sdate.month) + str(sdate.day)

#scraperwiki.sqlite.execute('drop table if exists `swdata`')
html1 = scraperwiki.scrape("http://lvbp.com/estadisticas_gen.asp?t=lanz&tipo=s&co_temporada=1&co_ano_temporada=6")
soup1 = BeautifulSoup(html1)
       
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
        record['JJ'] = int(columns[2].text)
        record['JI'] = int(columns[3].text)
        record['JG'] = int(columns[4].text)
        record['JP'] = int(columns[5].text)
        record['PCT'] = columns[6].text
        record['JS'] = int(columns[7].text)
        record['JC'] = int(columns[8].text)
        record['JB'] = int(columns[9].text)
        ip_split = columns[10].text.split('.')
        record['IP'] = int(ip_split[0]) + (int(ip_split[1]) * 0.1)
        record['H'] = int(columns[11].text)
        record['H2'] = int(columns[12].text)
        record['H3'] = int(columns[13].text)
        record['HR'] = int(columns[14].text)
        record['CP'] = int(columns[15].text)
        record['CL'] = int(columns[16].text)
        record['BB'] = int(columns[17].text)
        record['SO'] = int(columns[18].text)
        record['GP'] = int(columns[19].text)
        record['WP'] = int(columns[20].text)
        record['BK'] = int(columns[21].text)
        efe_split = columns[22].text.split('.')
        record['EFE'] = int(efe_split[0]) + (int(efe_split[1]) * 0.1)
        record['FECHA'] = int(sdate_split)
        record['key'] = sdate_split + columns[1].text + columns[0].text
        #print record
        if record.has_key('key'):
              # save records to the datastore
              scraperwiki.sqlite.save(["key"], record)



