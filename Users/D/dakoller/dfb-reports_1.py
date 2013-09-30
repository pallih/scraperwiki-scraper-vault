from pprint import pprint
import scraperwiki           
import lxml.html
import urllib2
import urlparse

def get_game_data(spieltag, spielid, saison= 12, saisonl=2012, liga = 'bl1f'):

    url = 'http://www.dfb.de/index.php?id=512335&no_cache=1&action=showSchema&lang=D&liga=%s&saison=%0d&saisonl=%0d&spieltag=%0d&spielid=%0d' % (liga,saison,saisonl,spieltag,spielid)

    #url = 'http://www.dfb.de/index.php?id=500028&no_cache=1&action=showSchema&lang=D&liga=bl1f&saison=12&saisonl=2012&spieltag=20&spielid=2136&cHash=94d96479c36165677cffe11cca8e4962'
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    params= urlparse.parse_qs(url)

    print(url)
    
    
    game_record = {}
    
    
    
    teams={}
    for tr in root.cssselect("tr.bundesliga_schema_team_header td"):
        #teams.append(tr.text)
        #print('tr')
        #pprint(tr.tag)
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
                    try:
                        players2.append(pl1a[1][:-1] +'//'+pl1a[0]+'//120' )
                    except Exception as e:
                        pprint(e)

    
                else:
                    players2.append(pl + '//1//120')
                    
    
    
        teams[tr.text] = players2
    
    #pprint(teams)    
    
    #game_record['teams'] = teams
    
    # get viewers
    #goals_sel =  root.cssselect("td.bundesliga_schema_stats")[0].getparent()
    #goals_sel = goals_sel.getchildren()[2]
    
    #viewers= ''
    
    #for ch in goals_sel:
    #    viewers =ch.cssselect("pre")[0].text
    #game_record['viewers'] = viewers 
    
    # get goals
    goals=[]
    goals_sel = root.cssselect("td.bundesliga_schema_stats")[1].getparent()
    goals_sel = goals_sel.getchildren()[2]
    
    
    for ch in goals_sel:
        if (ch.cssselect("pre")[0].text):
            goals= (ch.cssselect("pre")[0].text).split('\n')
    
    #pprint(goals)
    #game_record['goals'] = goals
    
    # referee
    
    #ref= ''
    #goals_sel =  root.cssselect("td.bundesliga_schema_stats")[2].getparent()
    #goals_sel = goals_sel.getchildren()[2]
    
    #ref = (goals_sel.text.replace('\n',',').replace(',',''))
    
    data = {
        'liga' : params['liga'][0],
        'saisonl' : int(params['saisonl'][0]), 
        'saison' : int(params['saison'][0]),
        'spielid' : int(params['spielid'][0]), 
        'spieltag' : int(params['spieltag'][0])}
    
    #game_record['referee'] = ref
    
    #game_record['params'] = data
    
    #pprint(game_record)
    
     #save to sqlite
    
    unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','score']
    
    
    for g in goals:

        g1 = g.split(' ')
        #pprint(g1)

        data2= { 'score': g1[0], 'player': g1[1], 'minute': g1[2] }
        data2 = dict(data.items() + data2.items())
    
        scraperwiki.sqlite.save(unique_keys, data2, table_name="goals")
    
    #unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','goal']
    
    
    # save teams
    
    unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','team','player']
    
    for tk,tv in teams.items():
        data2= {'team': tk}
    
        #pprint(tv)
    
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



def get_daylist(saison= 12, saisonl=2012, liga = 'bl1f'):    

    ds = range(1,17)

    #for day in days:
    for day in ds:

        url = 'http://www.dfb.de/index.php?id=512335&action=showDay&lang=D&liga=%s&saison=%0d&saisonl=%0d&spieltag=%0d&cHash=3c6d1afffaefe8d83c5604ba8482f433' % (liga,saison,saisonl,day )

        pprint(url)

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)        

        gamelink_table = root.cssselect("table.bundesliga_overview")[0]

        gamelinks = gamelink_table.cssselect("a")
        for gamelink in gamelinks:
            link = gamelink.attrib['href']

            fields = urlparse.parse_qs(link)
        
            get_game_data(spieltag = int(fields['spieltag'][0]), 
                spielid = int(fields['spielid'][0]), 
                saison =int(fields['saison'][0]), 
                saisonl = int(fields['saisonl'][0]), 
                liga = fields['liga'][0])



        



get_daylist()




from pprint import pprint
import scraperwiki           
import lxml.html
import urllib2
import urlparse

def get_game_data(spieltag, spielid, saison= 12, saisonl=2012, liga = 'bl1f'):

    url = 'http://www.dfb.de/index.php?id=512335&no_cache=1&action=showSchema&lang=D&liga=%s&saison=%0d&saisonl=%0d&spieltag=%0d&spielid=%0d' % (liga,saison,saisonl,spieltag,spielid)

    #url = 'http://www.dfb.de/index.php?id=500028&no_cache=1&action=showSchema&lang=D&liga=bl1f&saison=12&saisonl=2012&spieltag=20&spielid=2136&cHash=94d96479c36165677cffe11cca8e4962'
    
    html = scraperwiki.scrape(url)
    root = lxml.html.fromstring(html)
    
    params= urlparse.parse_qs(url)

    print(url)
    
    
    game_record = {}
    
    
    
    teams={}
    for tr in root.cssselect("tr.bundesliga_schema_team_header td"):
        #teams.append(tr.text)
        #print('tr')
        #pprint(tr.tag)
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
                    try:
                        players2.append(pl1a[1][:-1] +'//'+pl1a[0]+'//120' )
                    except Exception as e:
                        pprint(e)

    
                else:
                    players2.append(pl + '//1//120')
                    
    
    
        teams[tr.text] = players2
    
    #pprint(teams)    
    
    #game_record['teams'] = teams
    
    # get viewers
    #goals_sel =  root.cssselect("td.bundesliga_schema_stats")[0].getparent()
    #goals_sel = goals_sel.getchildren()[2]
    
    #viewers= ''
    
    #for ch in goals_sel:
    #    viewers =ch.cssselect("pre")[0].text
    #game_record['viewers'] = viewers 
    
    # get goals
    goals=[]
    goals_sel = root.cssselect("td.bundesliga_schema_stats")[1].getparent()
    goals_sel = goals_sel.getchildren()[2]
    
    
    for ch in goals_sel:
        if (ch.cssselect("pre")[0].text):
            goals= (ch.cssselect("pre")[0].text).split('\n')
    
    #pprint(goals)
    #game_record['goals'] = goals
    
    # referee
    
    #ref= ''
    #goals_sel =  root.cssselect("td.bundesliga_schema_stats")[2].getparent()
    #goals_sel = goals_sel.getchildren()[2]
    
    #ref = (goals_sel.text.replace('\n',',').replace(',',''))
    
    data = {
        'liga' : params['liga'][0],
        'saisonl' : int(params['saisonl'][0]), 
        'saison' : int(params['saison'][0]),
        'spielid' : int(params['spielid'][0]), 
        'spieltag' : int(params['spieltag'][0])}
    
    #game_record['referee'] = ref
    
    #game_record['params'] = data
    
    #pprint(game_record)
    
     #save to sqlite
    
    unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','score']
    
    
    for g in goals:

        g1 = g.split(' ')
        #pprint(g1)

        data2= { 'score': g1[0], 'player': g1[1], 'minute': g1[2] }
        data2 = dict(data.items() + data2.items())
    
        scraperwiki.sqlite.save(unique_keys, data2, table_name="goals")
    
    #unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','goal']
    
    
    # save teams
    
    unique_keys = ['liga', 'saisonl', 'spielid', 'spieltag','team','player']
    
    for tk,tv in teams.items():
        data2= {'team': tk}
    
        #pprint(tv)
    
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



def get_daylist(saison= 12, saisonl=2012, liga = 'bl1f'):    

    ds = range(1,17)

    #for day in days:
    for day in ds:

        url = 'http://www.dfb.de/index.php?id=512335&action=showDay&lang=D&liga=%s&saison=%0d&saisonl=%0d&spieltag=%0d&cHash=3c6d1afffaefe8d83c5604ba8482f433' % (liga,saison,saisonl,day )

        pprint(url)

        html = scraperwiki.scrape(url)
        root = lxml.html.fromstring(html)        

        gamelink_table = root.cssselect("table.bundesliga_overview")[0]

        gamelinks = gamelink_table.cssselect("a")
        for gamelink in gamelinks:
            link = gamelink.attrib['href']

            fields = urlparse.parse_qs(link)
        
            get_game_data(spieltag = int(fields['spieltag'][0]), 
                spielid = int(fields['spielid'][0]), 
                saison =int(fields['saison'][0]), 
                saisonl = int(fields['saisonl'][0]), 
                liga = fields['liga'][0])



        



get_daylist()




