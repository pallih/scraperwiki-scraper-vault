url= 'http://www.dfb.de/index.php?id=500028&no_cache=1&action=showSchema&lang=D&liga=bl1f&saison=12&saisonl=2012&spieltag=15&spielid=2108&cHash=23fb4e6276f05b7d3a4b8a6be2df443c'
from pprint import pprint
import scraperwiki           
html = scraperwiki.scrape(url)
#print html

import lxml.html
root = lxml.html.fromstring(html)

params={}
ps = url[(url.find('?')+1):].split('&')
for p in ps:
    k,v = p.split('=')
    params[k] = v


#print(params)


game_record = {}



teams={}
for tr in root.cssselect("tr.bundesliga_schema_team_header td"):
    #teams.append(tr.text)

    tr2= tr.getparent().getnext()

    for tr3 in tr2.getchildren():
        #pprint(tr3.tag)
        tr4 = tr3.getchildren()[0].getchildren()[0].getchildren()[0].getchildren()[0].getchildren()[0]
        players= tr4.text.replace(' ','').replace('\n',',').split(',')

        players2 = []
        for pl in players:
            if '(' in pl:
                pl1 = pl.split('(')
                pl1a = pl1[1].split('.')
                players2.append(pl1[0]+'//1//'+pl1a[0] )

                players2.append(pl1a[1][:-1] +'//'+pl1a[0]+'//120' )

            else:
                players2.append(pl + '//1//120')
                


    teams[tr.text] = players2
    

game_record['teams'] = teams

# get viewers
goals_sel =  root.cssselect("td.bundesliga_schema_stats")[0].getparent()
goals_sel = goals_sel.getchildren()[2]

viewers= ''

for ch in goals_sel:
    viewers =ch.cssselect("pre")[0].text
game_record['viewers'] = viewers 

# get goals
goals_sel =  root.cssselect("td.bundesliga_schema_stats")[1].getparent()
goals_sel = goals_sel.getchildren()[2]


for ch in goals_sel:
    goals= (ch.cssselect("pre")[0].text).split('\n')

#pprint(goals)
game_record['goals'] = goals

# referee

ref= ''
goals_sel =  root.cssselect("td.bundesliga_schema_stats")[2].getparent()
goals_sel = goals_sel.getchildren()[2]

ref = (goals_sel.text.replace('\n',',').replace(',',''))

data = {
    'liga' : params['liga'],
    'saisonl' : params['saisonl'], 
    'spielid' : params['spielid'], 
    'spieltag' : params['spieltag']}

game_record['referee'] = ref

game_record['params'] = data

pprint(game_record)

 #save to sqlite

unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','goal']


for g in goals:
    data2= {'goal': g}
    data2 = dict(data.items() + data2.items())

    scraperwiki.sqlite.save(unique_keys, data2, table_name="goals")

unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','goal']


# save teams

unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','team','player']

for tk,tv in teams.items():
    data2= {'team': tk}

    pprint(tv)

    for pl in tv:
        data2['player'] = pl.split('//')[0]
        data2['from'] = pl.split('//')[1]

        to1 = pl.split('//')[2]
        if to1 == '120':
            data2['to'] = ''
        else:
            data2['to'] = to1


        data2 = dict(data.items() + data2.items())

        scraperwiki.sqlite.save(unique_keys, data2, table_name="players")











url= 'http://www.dfb.de/index.php?id=500028&no_cache=1&action=showSchema&lang=D&liga=bl1f&saison=12&saisonl=2012&spieltag=15&spielid=2108&cHash=23fb4e6276f05b7d3a4b8a6be2df443c'
from pprint import pprint
import scraperwiki           
html = scraperwiki.scrape(url)
#print html

import lxml.html
root = lxml.html.fromstring(html)

params={}
ps = url[(url.find('?')+1):].split('&')
for p in ps:
    k,v = p.split('=')
    params[k] = v


#print(params)


game_record = {}



teams={}
for tr in root.cssselect("tr.bundesliga_schema_team_header td"):
    #teams.append(tr.text)

    tr2= tr.getparent().getnext()

    for tr3 in tr2.getchildren():
        #pprint(tr3.tag)
        tr4 = tr3.getchildren()[0].getchildren()[0].getchildren()[0].getchildren()[0].getchildren()[0]
        players= tr4.text.replace(' ','').replace('\n',',').split(',')

        players2 = []
        for pl in players:
            if '(' in pl:
                pl1 = pl.split('(')
                pl1a = pl1[1].split('.')
                players2.append(pl1[0]+'//1//'+pl1a[0] )

                players2.append(pl1a[1][:-1] +'//'+pl1a[0]+'//120' )

            else:
                players2.append(pl + '//1//120')
                


    teams[tr.text] = players2
    

game_record['teams'] = teams

# get viewers
goals_sel =  root.cssselect("td.bundesliga_schema_stats")[0].getparent()
goals_sel = goals_sel.getchildren()[2]

viewers= ''

for ch in goals_sel:
    viewers =ch.cssselect("pre")[0].text
game_record['viewers'] = viewers 

# get goals
goals_sel =  root.cssselect("td.bundesliga_schema_stats")[1].getparent()
goals_sel = goals_sel.getchildren()[2]


for ch in goals_sel:
    goals= (ch.cssselect("pre")[0].text).split('\n')

#pprint(goals)
game_record['goals'] = goals

# referee

ref= ''
goals_sel =  root.cssselect("td.bundesliga_schema_stats")[2].getparent()
goals_sel = goals_sel.getchildren()[2]

ref = (goals_sel.text.replace('\n',',').replace(',',''))

data = {
    'liga' : params['liga'],
    'saisonl' : params['saisonl'], 
    'spielid' : params['spielid'], 
    'spieltag' : params['spieltag']}

game_record['referee'] = ref

game_record['params'] = data

pprint(game_record)

 #save to sqlite

unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','goal']


for g in goals:
    data2= {'goal': g}
    data2 = dict(data.items() + data2.items())

    scraperwiki.sqlite.save(unique_keys, data2, table_name="goals")

unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','goal']


# save teams

unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','team','player']

for tk,tv in teams.items():
    data2= {'team': tk}

    pprint(tv)

    for pl in tv:
        data2['player'] = pl.split('//')[0]
        data2['from'] = pl.split('//')[1]

        to1 = pl.split('//')[2]
        if to1 == '120':
            data2['to'] = ''
        else:
            data2['to'] = to1


        data2 = dict(data.items() + data2.items())

        scraperwiki.sqlite.save(unique_keys, data2, table_name="players")











