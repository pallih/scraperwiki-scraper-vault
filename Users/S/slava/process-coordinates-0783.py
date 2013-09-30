import scraperwiki
import re

html = scraperwiki.scrape("http://www.royal-bank.ru/common/js/ymap.js")
#root = lxml.html.fromstring(html)

#pc = re.compile('^(\d+)?,', re.U | re.I)
#region = re.compile(', (.+)?(обл\.|область|рег|край)', re.U | re.I)
#city = re.compile('(г\.|г\.\ |город\ |город)(.+?),(.+)', re.U | re.I)

#address = re.compile("new ymaps.Placemark\(\[([\d\.]+?),([\d\.]+?)\]\,\ \{.*?balloonContent: '(.+?)'", re.U | re.I | re.S);
x_re = re.compile("'X' :(.+?),", re.U | re.I )
y_re = re.compile("'Y' :(.+?),", re.U | re.I )
name_re = re.compile("""'DESCR' : "(.+?)",""", re.U | re.I )

#html = html.decode('windows-1251').encode('utf-8')
x = x_re.findall(html)
y = y_re.findall(html)
name = name_re.findall(html.decode('windows-1251').encode('utf-8'))


for i in range(22):
    print i
    if len(name[i])>0:
        names = name[i].split("<br>")
    scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i+1,'lat': y[i], 'lon':x[i],'region':names[0], 'branch_name':name[i].replace(names[len(names)-1],""), 'street':names[len(names)-1]}, table_name="coordonate_adrese")

        


import scraperwiki
import re

html = scraperwiki.scrape("http://www.royal-bank.ru/common/js/ymap.js")
#root = lxml.html.fromstring(html)

#pc = re.compile('^(\d+)?,', re.U | re.I)
#region = re.compile(', (.+)?(обл\.|область|рег|край)', re.U | re.I)
#city = re.compile('(г\.|г\.\ |город\ |город)(.+?),(.+)', re.U | re.I)

#address = re.compile("new ymaps.Placemark\(\[([\d\.]+?),([\d\.]+?)\]\,\ \{.*?balloonContent: '(.+?)'", re.U | re.I | re.S);
x_re = re.compile("'X' :(.+?),", re.U | re.I )
y_re = re.compile("'Y' :(.+?),", re.U | re.I )
name_re = re.compile("""'DESCR' : "(.+?)",""", re.U | re.I )

#html = html.decode('windows-1251').encode('utf-8')
x = x_re.findall(html)
y = y_re.findall(html)
name = name_re.findall(html.decode('windows-1251').encode('utf-8'))


for i in range(22):
    print i
    if len(name[i])>0:
        names = name[i].split("<br>")
    scraperwiki.sqlite.save(unique_keys=['id'], data={'id':i+1,'lat': y[i], 'lon':x[i],'region':names[0], 'branch_name':name[i].replace(names[len(names)-1],""), 'street':names[len(names)-1]}, table_name="coordonate_adrese")

        


