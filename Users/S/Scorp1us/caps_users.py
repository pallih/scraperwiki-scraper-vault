import scraperwiki
import lxml.html
import time


def getUsers():
    html = scraperwiki.scrape("http://caps.fool.com/PlayerRankings.aspx?filter=20&sortcol=5&sortdir=1&source=ifltnvsnv0000001")
    root = lxml.html.fromstring(html)
    rows= root.xpath(".//*[@id='ctl00_cphMaster_ctlViewMorePlayers_dtgPlayers']/tr[position() > 1]/td[2]/a")
    users =[]
    for row in rows:
        username = row.text.strip()
        users.append(username)
        data={'who':username, 'start_date': '%d%d%d' % time.localtime(time.time())[0:3], 'end_date':None }
        print data
        scraperwiki.sqlite.save(unique_keys=['start_date', 'who'],data=data)

   
    return users  

getUsers()
