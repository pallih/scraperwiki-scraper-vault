import scraperwiki
import lxml.html
import string
import dateutil.parser
import time

startYear = 1987
endYear = 2012

for year in range(startYear, endYear + 1):
    
    print "Parsing " + str(year)
    round = ""

    html = scraperwiki.scrape("http://www.footywire.com/afl/footy/ft_match_list?year=" + str(year))

    root = lxml.html.fromstring(html)
    
    for tr in root.cssselect("div[class='datadiv'] tr"):
        tds = tr.cssselect("td[class='tbtitle']")
        if len(tds)==1:
            round = tds[0].text_content().strip()

        tds = tr.cssselect("td[class='data']")
        if len(tds)==7:
            venue = tds[2].text_content()
            attendance = tds[3].text_content()
    
            if venue == "BYE":
                continue
    
            teams = tds[1].cssselect("a")
            result = tds[4].cssselect("a")
            results = ["", ""];
            
            if len(result) == 1:
                result = result[0].text_content()
                
                if result != "":
                    results = string.split(result, "-")

            dateStr = tds[0].text_content()
            matchDate = dateutil.parser.parse(dateStr + " " + str(year))
            matchDate = time.mktime(matchDate.timetuple())
            
            data = {
                'round' : round,
                'date' : int(matchDate),
                'venue' : venue,
                'home' : teams[0].text_content(),
                'away' : teams[1].text_content(),
            }

            attendance = tds[3].text_content()
            homeScore = results[0]
            awayScore = results[1]

            if attendance != "":
                data['attendance'] = int(attendance)
                data['homeScore'] = int(homeScore)
                data['awayScore'] = int(awayScore)
            
            scraperwiki.sqlite.save(unique_keys=['date', 'home', 'away'], data=data, table_name='Match')