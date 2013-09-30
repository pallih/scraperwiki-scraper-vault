import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://seattle.mariners.mlb.com/team/roster_40man.jsp?c_id=sea")
root = lxml.html.fromstring(html)
for el in root.cssselect(".teamtableresults tbody tr .playerName a"):
   playername = el.text
   if playername is not None:
       thedata= el.getparent()
       thedata1= thedata.getnext()
       print playername
       if thedata1.text is not None:
           data = {
            'Player Name' : playername,
            'Bats/Throws' : thedata1.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['Player name'], data=data)
import scraperwiki           
import lxml.html
html = scraperwiki.scrape("http://seattle.mariners.mlb.com/team/roster_40man.jsp?c_id=sea")
root = lxml.html.fromstring(html)
for el in root.cssselect(".teamtableresults tbody tr .playerName a"):
   playername = el.text
   if playername is not None:
       thedata= el.getparent()
       thedata1= thedata.getnext()
       print playername
       if thedata1.text is not None:
           data = {
            'Player Name' : playername,
            'Bats/Throws' : thedata1.text
                }
       print data
       scraperwiki.sqlite.save(unique_keys=['Player name'], data=data)
