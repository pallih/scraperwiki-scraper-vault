# Blank Python
import time,scraperwiki
scraperwiki.sqlite.attach("kfchat")



rowid = scraperwiki.sqlite.select('MAX(rowid) FROM swdata')
print rowid
print scraperwiki.sqlite.select('Nev, count(Nev) from swdata GROUP BY Nev ORDER BY COUNT(Nev) DESC')
rowid = rowid[0].get('MAX(rowid)')
rekord={}
hanyadika = 0
napvaltozas = 0
i = 0  
'''
print scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=108052')
if scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=108052') == []:
    print 'megvan'
else:
    print 'nem ez'

print scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=108051')

while napvaltozas <> 2:
 if scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=?',rowid) <> []:
     rekord[i] = scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=?',rowid)
     hanyadika = rekord[i][0].get('Datum')[:2]
     if i==0:
         oldh = rekord[i][0].get('Datum')[:2]
     if hanyadika <> oldh:
         napvaltozas+=1
         oldh = hanyadika
 print oldh, hanyadika, napvaltozas, i, rowid
 i+=1
 rowid-=1
'''
# Blank Python
import time,scraperwiki
scraperwiki.sqlite.attach("kfchat")



rowid = scraperwiki.sqlite.select('MAX(rowid) FROM swdata')
print rowid
print scraperwiki.sqlite.select('Nev, count(Nev) from swdata GROUP BY Nev ORDER BY COUNT(Nev) DESC')
rowid = rowid[0].get('MAX(rowid)')
rekord={}
hanyadika = 0
napvaltozas = 0
i = 0  
'''
print scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=108052')
if scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=108052') == []:
    print 'megvan'
else:
    print 'nem ez'

print scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=108051')

while napvaltozas <> 2:
 if scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=?',rowid) <> []:
     rekord[i] = scraperwiki.sqlite.select('datum,nev,text from swdata where rowid=?',rowid)
     hanyadika = rekord[i][0].get('Datum')[:2]
     if i==0:
         oldh = rekord[i][0].get('Datum')[:2]
     if hanyadika <> oldh:
         napvaltozas+=1
         oldh = hanyadika
 print oldh, hanyadika, napvaltozas, i, rowid
 i+=1
 rowid-=1
'''
