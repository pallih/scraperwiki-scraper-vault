import scraperwiki
import datetime
import lxml.html      
rows = []

M = {
'января': 1,
'февраля' : 2,
'марта' : 3,
'апреля': 4,
'мая' : 5,
'июня' : 6,
'июля' : 7,
'августа' : 8,
'сентября' : 9,
'октября' : 10,
'ноября' : 11,
'декабря' : 12
}




print "hello"
html = scraperwiki.scrape("http://gibddmoscow.ru/")

root = lxml.html.fromstring(html)
base = root.cssselect('div [class ="b-block b-stat"]')[0]
head = base.cssselect('h2')
head = base.cssselect('span')


tot = base.cssselect('div [class="small"]')[0]

Date = head[0].text

temp = Date[3:]
print temp

Dyear = int(temp[len(Date)-7:])
print Dyear
Dday = int(temp[:2])
print Dday

x = Date.split()[2].encode('utf-8', 'ignore')
Dmonth = M[x]
print 'month:', Dmonth


D = datetime.date(Dyear, Dmonth, Dday)
Dweek = D.weekday()
print D



dtp = tot.cssselect('p')[0].cssselect('font')[0].text
if dtp == None:
    dtp = tot.cssselect('p')[0].text
print 'DTP: ', dtp

total = tot[0].text[18:-5]
#print total


tables = base.cssselect('table')

Avaries = tables[2].cssselect('font')[0].text
#print Avaries.text 


casulties = tables[0].cssselect('font')

wounded = casulties[3].text
deaths = casulties[0].text

childDeath = casulties[1].text
if childDeath == None:
    childDeath = casulties[1].cssselect('b')[0].text

print 'детей умерло: ', childDeath

childWound = casulties[4].text

if childWound == None:
    childWound = casulties[1].cssselect('b')[0].text

print 'детей ранено: ', childWound


#for i in range (len(casulties)):
#    print casulties[i].text

alchogol = tables[1].cssselect('font')[0].text
if alchogol == None:
    alchogol = tables[1].cssselect('font')[0].cssselect('b')[0].text

ugon = tables[1].cssselect('font')[1].text
if ugon == None:
    ugon = tables[1].cssselect('font')[1].cssselect('strong')[0].text



print 'водителей в состоянии алкогольного опьянения задержано: ', alchogol
print 'найдено ранее угнаных машин:', ugon

data = {
's_DTP': dtp,
'date': D,
'avaries': int(Avaries),
'alchogol': int(alchogol),
'ugon': int(ugon),
'deaths': int(deaths),
'childDeaths':int(childDeath),
'wounded': int(wounded),
'childWounded': int(childWound),
'weekday': Dweek
}

scraperwiki.sqlite.save(unique_keys=['date'], data=data)
