# -*- coding: utf-8 -*-
import urllib2
import re
from BeautifulSoup import BeautifulSoup, Comment
from datetime import datetime, timedelta
import htmlentitydefs
from BeautifulSoup import BeautifulStoneSoup
import sys

import scraperwiki

# Blank Python
stdin = sys.stdin
stdout = sys.stdout
reload(sys)
sys.setdefaultencoding('utf-8')
sys.stdin = stdin
sys.stdout = stdout

def htmlentity2unicode(text):
    reference_regex = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
    num16_regex = re.compile(u'#x\d+', re.IGNORECASE)
    num10_regex = re.compile(u'#\d+', re.IGNORECASE)

    result = u''
    i = 0
    while True:
        match = reference_regex.search(text, i)
        if match is None:
            result += text[i:]
            break

        result += text[i:match.start()]
        i = match.end()
        name = match.group(1)

        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])
        elif num16_regex.match(name):
            result += unichr(int(u'0'+name[1:], 16))
        elif num10_regex.match(name):
            result += unichr(int(name[1:]))

    return result
    
def parseDate(s):
    ss = s.split()
    m, d = ss[0].split('/')
    sh, sm = ss[2].split(':')
    eh, em = ss[4].split(':')
    if m and d and sh and sm and eh and em:
        try:
            ds = datetime(datetime.today().year, int(m), int(d), int(sh), int(sm))
            de = datetime(datetime.today().year, int(m), int(d), int(eh), int(em))
        except:
            print ds , de
            return False

        if int(int(sh) > int(eh)):
            de = de + timedelta(1)

        return ds, de
    else:
        return False

def makeDate(n):
    day = datetime.today() + timedelta(n) + timedelta(hours=9)
    date = day.strftime("%Y%m%d") + '0500'
    return date

def isIDin(id):
    if id in IDTable:
        return True
    return False

def getChijou(n):
    date = makeDate(n)
    url = 'http://tv.so-net.ne.jp/chart/catv/jcom/3/chart.action?head=' + date
    print url

    req = urllib2.Request(url)
    req.add_header('Cookie', 'gtv.catvStationAreaId=3; gtv.span=24')
    c = urllib2.urlopen(req).read()
    return c

def getBS(ch, n):
    date = makeDate(n)
    url = 'http://tv.so-net.ne.jp/chart/bs' + ch + '.action?head=' + date
    print url

    req = urllib2.Request(url)
    req.add_header('Cookie', 'gtv.span=24')
    try:
        c = urllib2.urlopen(req).read()
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
        return False
    return c

def getTimeTable(n):
    makeIDTable()
    for i in xrange(1,5):
        c = getBS(str(i), n)
        parseTimeTable(c)

    c = getChijou(n)
    parseTimeTable(c)

#def getTimeTable(n):
#    makeIDTable()
#    if modulename == 'tvTimeTableBS':
#        for i in range(1, 5):
#            c = getBS(str(i), n)
#            parseTimeTable(c)
#        if n > 6:
#            c = getChijou(n)
#            parseTimeTable(c)
#    else:
#        if n < 7:
#            c = getChijou(n)
#            parseTimeTable(c)

def makeIDTable():
    global IDTable

#    if scraperwiki.sqlite.show_tables() == False:
#        return False
    
#    c = scraperwiki.sqlite.execute('select count(*) FROM sqlite_master WHERE type="table" AND name="swdata"')
    c = execute('select count(*) FROM sqlite_master WHERE type="table" AND name="swdata"')
#    if c[0]['count(*)'] == 0:
    if c['data'][0][0] == 0:
        print 'empty swdata'
        return False
    dstart  = datetime.strptime(nowShori, '%Y%m%d%H%M').isoformat()
    dend = (datetime.strptime(nowShori, '%Y%m%d%H%M') + timedelta(hours=24)).isoformat()
    sql = "id from swdata where ((end > '%s' and end <= '%s') or (start >= '%s' and start < '%s'))" % (dstart , dend, dstart , dend)
    sql = sql + "and (not genre like '%野球%')"
    c = select(sql)
    for i in c:
        IDTable.append(i['id'])

def parseTimeTable(c):

    try:
        s = BeautifulSoup(c)
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
        return False

    c = str(s.find('div', id='chartColumn')).split('\n')
        
    for l in c:
        r = re.match(r'.+(/schedule/([0-9]+).action).+', l)
        if r:
            targetURL = 'http://tv.so-net.ne.jp' + r.group(1)
            id = r.group(2)
            getProgram(id, targetURL)
    
def getProgram(id, url):

    if isIDin(id):
        return

    req = urllib2.Request(url)
    try:
        c = urllib2.urlopen(req).read()
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
        return False

    c = htmlentity2unicode(c)
    s = BeautifulSoup(c)
    f = s.find('div', {'class': 'contBlock utileSetting'})
    if f is None:
        print "NoneType Error:", id
        return False
    fs = f.findAll('dd');
    shosai = ((s.findAll('div', {'class': 'contBlock subUtileSetting'}))[1].find('p', {'class': 'basicTxt'})).renderContents()

    shosai = shosai.replace('<br />' , '').replace('\r', '').replace('\n', '').replace('\t', '')

    #title
    if fs[0]:
        title =  htmlentity2unicode(fs[0].contents[0])

    #date
    if fs[1]:
        date = parseDate(fs[1].contents[0])

        if date == False:
            print "date parse ERROR", id
            return False

    #ch
    if fs[2]:
        ch  = fs[2].contents[0]
        m = ch_regex.match(ch)
        if m:
            ch = m.group(1)
    #genre
    if fs[3]:
        genre = ''
        g =  fs[3].findAll('a')
        for i in g:
            genre = genre + i.string + ' '

#    print 'title:' + title ,
#    print ' date:'  + date[0].isoformat() ,
#    print ' ch:' + ch
    try:
        scraperwiki.sqlite.save(unique_keys=["id"], data={"id":id, "title":title, "start":date[0], "end":date[1], "ch":ch, "genre":genre, "shosai":shosai, "urlDate":nowShori})
    except:
        return False

def select(sql):
    try:
        c = scraperwiki.sqlite.select(sql)
        return c
    except scraperwiki.Error:
        print "scraperwiki.Error", sys.exc_info()[0], ':' , sys.exc_info()[1]
        return False

def execute(sql):
#    print sql
    try:
        c = scraperwiki.sqlite.execute(sql)
        return c
    except scraperwiki.Error:
        print "scraperwiki.exexute.Error", sys.exc_info()[0], ':' , sys.exc_info()[1]
        return False
    
class e2:
    chs = {'GAORA':'500254', 'スカイ・A　sports＋':'500250', '朝日ニュースターＨＤ':'500299'}
    
    def __init__(self):
        deleteOld()
        self.get_e2()

    def get_e2(self):
#'400302' GAORA
#'500250' A+
        for chName, ch in self.chs.iteritems():
            self.makeIDTable(chName)
            url = "http://tv.so-net.ne.jp/chart/cs110/" + ch + ".action"
            print url

            req = urllib2.Request(url)
            req.add_header('Cookie', 'gtv.span=24')
            try:
                c = urllib2.urlopen(req).read()
                parseTimeTable(c)
            except:
                print sys.exc_info()[0], sys.exc_info()[1]
                continue
#                return False
        return c

    def makeIDTable(self, ch):
        global IDTable
        IDTable = []

#        if scraperwiki.sqlite.show_tables() == False:
#            return False
        
        c = select('count(*) FROM sqlite_master WHERE type="table" AND name="swdata"')
        if c[0]['count(*)'] == 0:
            print 'empty swdata'
            return False

#        sql = "id,title from swdata where ch='%s'" % (ch)
#        sql = sql + " and (not genre like '%野球%')"
        sql = "id from swdata where ch='%s'" % (ch)
        sql = sql + " and (not genre like '%野球%')"
#        sql = sql + "union select id from mlbjpgyao.swdata where ch='%s'" % (ch)
        sql = sql + "union select id from swdata where ch='%s'" % (ch)
        sql = sql + " and (not genre like '%野球%')"
        c = select(sql)
        for i in c:
            IDTable.append(i['id'])

def deleteOld():
    try:
        day = datetime.today() + timedelta(-1) + timedelta(hours=9)
        target = day.isoformat()
        print target
        c = scraperwiki.sqlite.execute("delete from swdata where end < '" + target + "'")
        scraperwiki.sqlite.commit()
#        print c        
#        if len(c['data']) == 0:
#            print "no data deleted"
#            return False
#        else:
#            print 'len:' , len(c['data'])
        return True
    except:
        print sys.exc_info()[0], sys.exc_info()[1]
        return False

class bs1:
    def makeURL(self):
#http://cgi4.nhk.or.jp/hensei/program/query.cgi?area=001&time_start=20120528&time_end=20120604&cht=2&chr=&category_select=cs_01&chc=0101&qt=mlb&cho=&offset=1
        for n in xrange(3):
            url = 'http://cgi4.nhk.or.jp/hensei/program/query.cgi?area=001&cht=2&chr=&category_select=cs_01&chc=0101&qt=mlb&cho=&offset=' + str(n)
            req = urllib2.Request(url)
            c = urllib2.urlopen(req).read()
            self.parse(c)

    def parse(self,c):
        s = BeautifulSoup(c)
        tab = s.find('table')
        if tab == None:
            return
        f = tab.findAll('tr')
        for i in f:
            j = i.findAll('td')
            if j:
                day = j[0].contents[0].string.strip()
                t = j[0].contents[2].string.strip()
                ch = j[1].string
#                if ch == 'BS1(102)':
#                    continue
                title = j[2]
                r = re.match(r'([0-9]+)月([0-9]+)日.+', day.encode('utf-8'))
                m = int(r.group(1))
                d = int(r.group(2))
                r = re.match(r'(午前|午後)([0-9]+):([0-9]+)～([翌日]*)(午前|午後)([0-9]+):([0-9]+)\((\d+)分\)', t.encode('utf-8'))
                s_noon = r.group(1)
                s_h = int(r.group(2))
                if s_noon == '午後':
                    s_h = s_h + 12
                s_m = int(r.group(3))
                e_yokujitu = r.group(4)

                e_noon = r.group(5)
                e_h = int(r.group(6))
                if e_noon == '午後':
                    e_h = e_h + 12
                e_m = int(r.group(7))
                s = int(r.group(8))

                if s < 49:
                    continue
                ds = datetime(datetime.today().year, m, d, s_h, s_m)
                if e_yokujitu == '翌日':
                    de = datetime(datetime.today().year, m, d+1, e_h, e_m)
                else:
                    de = datetime(datetime.today().year, m, d, e_h, e_m)
                
                title = htmlentity2unicode(title.a.contents[0])
                print ds, de, ch, title

#                scraperwiki.sqlite.save(unique_keys=["start"], data={"title":title, "start":ds, "end":de , "ch":"NHK-BS1"})
                scraperwiki.sqlite.save(unique_keys=["start"], data={"title":title, "start":ds, "end":de , "ch":ch}, table_name="etc")
        
    def __init__(self):
        self.makeURL()


class mlbtv:
    def makeURL(self):
        for n in xrange(7):
            day = datetime.today() + timedelta(n) + timedelta(hours=-11)
            #get json format mlb.tv schedule data
            url = 'http://mlb.mlb.com/gdcross/components/game/mlb/year_' + day.strftime("%Y") + '/month_' + day.strftime("%02m") + '/day_' + day.strftime("%02d")+ '/grid.json'
            print url
            try:
                req = urllib2.Request(url)
                c = urllib2.urlopen(req).read()
            except:
                print "urllib2 error", sys.exc_info()[0], ':' , sys.exc_info()[1], 'now:' , nowShori
                return

            event_time , home , away = self.decodeJSON(c)
            if event_time == False:
                print 'no free game day'
                continue
            print event_time + ' -> ' + home + ' vs ' + away
            h , m = (event_time.split())[0].split(':')
            h = int(h)
            if h == 12:
                h = 0
            start = datetime(day.year, day.month, day.day, h+12, int(m))
            start = start + timedelta(hours=13)
            end = start + timedelta(hours=3)
            scraperwiki.sqlite.save(unique_keys=["start"], data={"title":home + ' vs ' + away, "start":start, "end":end , "ch":"mlb.tv"}, table_name="etc")

    def decodeJSON(self,c):
        import json
        j = json.loads(c)
        if (not j.has_key('data')) or (not j['data'].has_key('games')) or (not j['data']['games'].has_key('game')) :
            return False,False,False
        it = j['data']['games']['game']
        if type(it) == dict:
            return False,False,False
        for i in it:
            home = ''
            away = ''
            event_time = ''
            free = False
            for k, v in i.items():
                if k == 'home_team_name':
                    home = v
                elif k == 'away_team_name':
                    away = v
                elif k == 'event_time':
                    event_time = v
                if k == 'game_media':
                    try:
                        for i2 in v['homebase']['media']:
                            for k3,v3 in i2.items():
                                if k3 == 'free' and v3 == 'ALL':
                                    free = True
                    except:
                        pass
            if free:                            
                return event_time , home , away
        return False,False,False

    def __init__(self):
        self.makeURL()

class gyao:
    def __init__(self):
#        self.deleteAll()
        req = urllib2.Request('http://gyao.yahoo.co.jp/mlb/live/')
        c = urllib2.urlopen(req).read()
        s = BeautifulSoup(c)
        f = s.find('div', id='program').find('table').findAll('tr')
        for i in f:
            j = i.findAll('td')
            if not j:
                continue
            d = datetime.strptime(j[0].string.replace(' ', '').strip() + '-' + j[1].string, u'%Y年%m月%d日-%H:%M')
            end = d  + timedelta(hours=3)
            title = '「%s」対「%s」' % (j[2].string ,j[3].string)
            print title
            try:
                scraperwiki.sqlite.save(unique_keys=["start"], data={"title":title, "start":d, "end":end , "ch":"GyaO"})
#                scraperwiki.sqlite.save(unique_keys=["start"], data={"title":title, "start":d, "end":end , "ch":"GyaO"}, table_name="etc")
            except:
                print "gyao save error:", d, sys.exc_info()[0], sys.exc_info()[1]
                continue

    def deleteAll(self):
        c = execute("drop table etc ")


#----------------------------
IDTable = []
ch_regex = re.compile('(.+)\(Ch\.[0-9]+\)')
nowShori = ''

def main():
    global nowShori
    
    allDone = False
    nowShori = scraperwiki.sqlite.get_var('daynum')

    print "nowShori set to 0"
    nowShori = ''
    print nowShori

    deleteOld()

    if nowShori == '':
        flag = True
    else:
        flag = False

    try:
        for i in range(5):
            target = makeDate(i)
#            print target
            if flag == False and target == nowShori:
                flag = True

            if flag == False:
                print "flag == False"
                continue

            nowShori = target
            print 'getTimetable:', i, nowShori
            getTimeTable(i)
    except scraperwiki.CPUTimeExceededError:
        print "exceed CPU", sys.exc_info()[0], ':' , sys.exc_info()[1], 'now:' , nowShori
        if allDone == False:
            scraperwiki.sqlite.save_var('daynum', nowShori)
        sys.exit()

    #all done reset
    nowShori = makeDate(7)
    allDone = True
    nowShori = ''

    scraperwiki.sqlite.save_var('daynum', nowShori)

if __name__ == 'scraper' or  __name__ == '__main__':
#    gyao()
    e2()
    main()

#    bs1()
#    mlbtv()

#    modulename = 'tvTimeTableBS'
#    modulename = 'mlb.jp@gyao'

