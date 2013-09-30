import scraperwiki
import lxml.html


# Blank Python
html = scraperwiki.scrape("http://www.fifa.com/worldfootball/worldmatchcentre/index.html")
#print html

root = lxml.html.fromstring(html)
#print root


match_details = "" 
home_team = ""
away_team = "" 
i = 0 
match_date = ""
match_result = ""
match_status = ""

for match in root.cssselect("div.wmcMatchContent"):
    match_details  = lxml.html.tostring(match)
    #Retrieve match status (FT or not)
    start = match_details.find("wmcResBoxCaption",0);
    start = start + len("wmcResBoxCaption>") + 1
    end = match_details.find("</div>",start);
    match_status = match_details[start:end]
    print match_status 

    if (match_status == "FT"):
        # Retrieve match date
        start = match_details.find("</div></div><div>",end)
        start = start + len("</div></div><div>")
        end = match_details.find("</div></span></div>",start)
        match_date = match_details[start:end]
        
    
        # Retrieve home team name
        start = match_details.find("wmcTeamName",end) + 2
        start = start + len("wmcTeamName") 
        end = match_details.find("</div>",start)
        home_team = match_details[start:end]
    
        #Retrieve match result
        start = match_details.find("wmcMR",end) + 2 
        start = start + len("wmcMR")
        end = match_details.find("</div>",start)
        match_result = match_details[start:end]
    
        #Retrieve away team
        start = match_details.find("wmcTeamName",end) + 2
        start = start + len("wmcTeamName") 
        end = match_details.find("</div>",start)
        away_team = match_details[start:end]
        #print match_date,"<- ->", home_team," MR ",match_result," ",away_team
        i = i + 1
    
        data = {
                'match_no' : i,
                'match_date' : match_date,
                'home_team'  : home_team,
                'away_team'  : away_team,
                'score'      : match_result
            }
    
        #print data
        scraperwiki.sqlite.save(unique_keys=['match_no'], data=data)


       







import scraperwiki
import lxml.html


# Blank Python
html = scraperwiki.scrape("http://www.fifa.com/worldfootball/worldmatchcentre/index.html")
#print html

root = lxml.html.fromstring(html)
#print root


match_details = "" 
home_team = ""
away_team = "" 
i = 0 
match_date = ""
match_result = ""
match_status = ""

for match in root.cssselect("div.wmcMatchContent"):
    match_details  = lxml.html.tostring(match)
    #Retrieve match status (FT or not)
    start = match_details.find("wmcResBoxCaption",0);
    start = start + len("wmcResBoxCaption>") + 1
    end = match_details.find("</div>",start);
    match_status = match_details[start:end]
    print match_status 

    if (match_status == "FT"):
        # Retrieve match date
        start = match_details.find("</div></div><div>",end)
        start = start + len("</div></div><div>")
        end = match_details.find("</div></span></div>",start)
        match_date = match_details[start:end]
        
    
        # Retrieve home team name
        start = match_details.find("wmcTeamName",end) + 2
        start = start + len("wmcTeamName") 
        end = match_details.find("</div>",start)
        home_team = match_details[start:end]
    
        #Retrieve match result
        start = match_details.find("wmcMR",end) + 2 
        start = start + len("wmcMR")
        end = match_details.find("</div>",start)
        match_result = match_details[start:end]
    
        #Retrieve away team
        start = match_details.find("wmcTeamName",end) + 2
        start = start + len("wmcTeamName") 
        end = match_details.find("</div>",start)
        away_team = match_details[start:end]
        #print match_date,"<- ->", home_team," MR ",match_result," ",away_team
        i = i + 1
    
        data = {
                'match_no' : i,
                'match_date' : match_date,
                'home_team'  : home_team,
                'away_team'  : away_team,
                'score'      : match_result
            }
    
        #print data
        scraperwiki.sqlite.save(unique_keys=['match_no'], data=data)


       







