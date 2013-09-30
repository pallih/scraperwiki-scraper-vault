import scraperwiki
import lxml.html

#Cycle through the years
year = 1992
while(year<2013):
        year = year + 1
    
        #Cycle Through Rounds in a Year
        cnt = 1
        while(cnt<22):
            round = "http://finalsiren.com/Results.asp?SeasonID=%d&Round=%d-1&Go=Go" % (year,cnt)
            ht = scraperwiki.scrape(round)
            cnt = cnt + 1
        
        #Cycles through the rounds matches
        
            while(ht.find('href="/MatchDetails.asp?GameID=')>0):
                test = ht.find('href="/MatchDetails.asp?GameID=')
                test2 = ht.find('>Details')
                match_ref = ht[(test+6):test2-1]
                st = match_ref.find('&amp;')
                match_ref2 = match_ref[0:st] + '&' + match_ref[st+5:]
                ht = ht[test2+10:]
                html = scraperwiki.scrape('http://finalsiren.com' + match_ref2)
                
                root = lxml.html.fromstring(html)
                
                test = html.find('href="/MatchDetails.asp?GameID=')
                test2 = html.find('&amp;Code=')
                match_code = html[(test+31):test2]
                
                for tr in root.cssselect("table[class='matchdetails'] tr"):
                        ths = tr.cssselect("h2")
                        if len(ths) == 2:
                            teams= {
                                'Home' : ths [0].text_content(),
                                'Away' : ths [1].text_content()
                                
                            }
                           
                
                team_sel = 'Home'
                opp_sel = 'Away'
                attend_s = html.find('Attendance:')
                attend_str = html[attend_s:]
                attend_f = attend_str.find('</nobr')
                attend = attend_str[12:attend_f]
                if attend=='':
                    attend='0'
        
                ground_s = html.find('Ground.asp?GroundID=')
                ground_str = html[ground_s:]
                ground_f = ground_str.find('"')
                ground = ground_str[20:ground_f]
        
                for tr in root.cssselect("table[class='playerstatssmall'] tr"):
                    tds = tr.cssselect("td")
                    if len(tds)==13:
                        data = {
                            'Player' : tds[0].text_content(),
                            'Kicks' : int(tds[1].text_content()),
                            'Handballs' : int(tds[2].text_content()),
                            'Disposals' : int(tds[3].text_content()),
                            'Marks' : int(tds[4].text_content()),
                            'Hitouts' : int(tds[5].text_content()),
                            'Takles' : int(tds[6].text_content()),
                            'Free_For' : int(tds[7].text_content()),
                            'Free_Against' : int(tds[8].text_content()),
                            'Goals' : int(tds[9].text_content()),
                            'Behinds' : int(tds[10].text_content()),
                            'Score' : int(tds[11].text_content()),
                            'Rating' : int(tds[12].text_content()),
                            'Match_Code' : match_code,
                            'Team' : teams[team_sel],
                            'Opponent' : teams[opp_sel],
                            'Key' : tds[0].text_content() + match_code,
                            'Round' : cnt,
                            'Year' : year,
                            'Attendance' : int(attend),
                            'Ground' : int(ground)
                        }
                        if tds[0].text_content()=='Totals':
                            team_sel = 'Away'
                            opp_sel = 'Home'
                
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                        
import scraperwiki
import lxml.html

#Cycle through the years
year = 1992
while(year<2013):
        year = year + 1
    
        #Cycle Through Rounds in a Year
        cnt = 1
        while(cnt<22):
            round = "http://finalsiren.com/Results.asp?SeasonID=%d&Round=%d-1&Go=Go" % (year,cnt)
            ht = scraperwiki.scrape(round)
            cnt = cnt + 1
        
        #Cycles through the rounds matches
        
            while(ht.find('href="/MatchDetails.asp?GameID=')>0):
                test = ht.find('href="/MatchDetails.asp?GameID=')
                test2 = ht.find('>Details')
                match_ref = ht[(test+6):test2-1]
                st = match_ref.find('&amp;')
                match_ref2 = match_ref[0:st] + '&' + match_ref[st+5:]
                ht = ht[test2+10:]
                html = scraperwiki.scrape('http://finalsiren.com' + match_ref2)
                
                root = lxml.html.fromstring(html)
                
                test = html.find('href="/MatchDetails.asp?GameID=')
                test2 = html.find('&amp;Code=')
                match_code = html[(test+31):test2]
                
                for tr in root.cssselect("table[class='matchdetails'] tr"):
                        ths = tr.cssselect("h2")
                        if len(ths) == 2:
                            teams= {
                                'Home' : ths [0].text_content(),
                                'Away' : ths [1].text_content()
                                
                            }
                           
                
                team_sel = 'Home'
                opp_sel = 'Away'
                attend_s = html.find('Attendance:')
                attend_str = html[attend_s:]
                attend_f = attend_str.find('</nobr')
                attend = attend_str[12:attend_f]
                if attend=='':
                    attend='0'
        
                ground_s = html.find('Ground.asp?GroundID=')
                ground_str = html[ground_s:]
                ground_f = ground_str.find('"')
                ground = ground_str[20:ground_f]
        
                for tr in root.cssselect("table[class='playerstatssmall'] tr"):
                    tds = tr.cssselect("td")
                    if len(tds)==13:
                        data = {
                            'Player' : tds[0].text_content(),
                            'Kicks' : int(tds[1].text_content()),
                            'Handballs' : int(tds[2].text_content()),
                            'Disposals' : int(tds[3].text_content()),
                            'Marks' : int(tds[4].text_content()),
                            'Hitouts' : int(tds[5].text_content()),
                            'Takles' : int(tds[6].text_content()),
                            'Free_For' : int(tds[7].text_content()),
                            'Free_Against' : int(tds[8].text_content()),
                            'Goals' : int(tds[9].text_content()),
                            'Behinds' : int(tds[10].text_content()),
                            'Score' : int(tds[11].text_content()),
                            'Rating' : int(tds[12].text_content()),
                            'Match_Code' : match_code,
                            'Team' : teams[team_sel],
                            'Opponent' : teams[opp_sel],
                            'Key' : tds[0].text_content() + match_code,
                            'Round' : cnt,
                            'Year' : year,
                            'Attendance' : int(attend),
                            'Ground' : int(ground)
                        }
                        if tds[0].text_content()=='Totals':
                            team_sel = 'Away'
                            opp_sel = 'Home'
                
                        scraperwiki.sqlite.save(unique_keys=['Key'], data=data)
                        
