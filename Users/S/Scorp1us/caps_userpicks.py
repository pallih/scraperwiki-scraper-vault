import scraperwiki
from urllib2 import HTTPError 
import lxml.html
import time

def fixDate(date):
    date = date.strip() 
    date = '20%s-%s-%s' % (date[-2:], date[0:2], date[3:5])
    return date

def updateRunData():
    scraperwiki.sqlite.execute("create table if not exists rssdata (ticker text, count integer, start_price real, date text)")
    scraperwiki.sqlite.execute("insert into rssdata (ticker, count, start_price, date) select ticker , count(ticker), start_price, datetime('now') date from swdata where call='Outperform' and stock_gain_pct >2 group by ticker having count(ticker) > 2")


def getUsers():
    users =[]
    for pagenum in range(1,10):
        html = None
        while html == None:
            try:
                html = scraperwiki.scrape("http://caps.fool.com/PlayerRankings.aspx?filter=20&sortcol=5&sortdir=1&source=ifltnvsnv0000001&pagenum=%d" % pagenum)
            except HTTPError, e:
                if e not in [400, 404, 500]:
                    raise e   
                time.sleep(5)    
            except URLError, e:
                time.sleep(5)

        root = lxml.html.fromstring(html)
        rows= root.xpath(".//*[@id='ctl00_cphMaster_ctlViewMorePlayers_dtgPlayers']/tr[position() > 1]/td[2]/a")
        if len(rows):
            
            for row in rows:
                username = row.text.strip()
                users.append(username)
                try:
                    scraperwiki.sqlite.save(['username'], {'username':username}, table_name="caps_users")
                except: 
                    pass
        time.sleep(5)
    return users  

def getUserPicks(username):
    # Blank Python
    html = None
    while html == None:
        try:    
            html = scraperwiki.scrape("http://caps.fool.com/player/%s.aspx" % username)
        except HTTPError, e: 
            if e not in [400, 404, 500]:
                raise e        
            time.sleep(5)
        except URLError, e:
            time.sleep(5)

    root = lxml.html.fromstring(html)
    rows= root.xpath("//table[@id='ctl00_cphMaster_ctlPlayers_dtgStockPicks']/tr[position() > 1]")
    #print len(rows)
    
    columns = ['top', 'start_date', 'ticker', 'caps_rating', 'call', 'duration', 'start_price', 'today', 'stock_gain_pct', 'index_gain_pct', 'score', 'pitch']
    rating_imgs = {
            'http://g.foolcdn.com/art/ratings/foolcaps_none.gif':'0', 
            'http://g.foolcdn.com/art/ratings/foolcaps_one.gif': '1', 
            'http://g.foolcdn.com/art/ratings/foolcaps_two.gif': '2', 
            'http://g.foolcdn.com/art/ratings/foolcaps_three.gif':'3',
            'http://g.foolcdn.com/art/ratings/foolcaps_four.gif': '4', 
            'http://g.foolcdn.com/art/ratings/foolcaps_five.gif': '5'}
    for row in rows:
        data = {}
        data['who'] = username
        cells = row.xpath('td')
        for i in range(len(cells)):
            column = columns[i]
            #print column
            if (column == 'start_date'):
                spans = cells[i].xpath('span')
                data[column] = fixDate(spans[0].text.strip())
            elif (column == 'ticker'):
                links = cells[i].xpath("span/a")
                data[column] = links[0].text           
            elif (column == 'call'):
                performances = cells[i].xpath("img[@title]")
                data[column] = performances[0].attrib["title"]
            elif (column == 'caps_rating'):
                src =  cells[i].xpath('img[@src]')
                data[column] = rating_imgs[src[0].attrib['src']]
            elif (column == 'top'):
                top = cells[i].xpath('span/a/img[@src]')
                data[column] = '1' if len(top) > 0 else '0'
                #print 'Top', data[column]
            else:
                value = row[i].text.strip()
                if len(value):
                    if value[0] == '$' or value[0] == '+':
                        value = value[1:]
                    if value[-1] == '%':
                        value = value[:-1]
                data[columns[i]] = value
    
        #print data
        try:
            scraperwiki.sqlite.save(unique_keys=['start_date', 'ticker', 'who'], data=data)
        except:
            pass

users=[]
while len(users) == 0:
    users = getUsers()
    for user in users:
        print user
        getUserPicks(user)
        time.sleep(5); 

updateRunData()
