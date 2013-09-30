#import urllib
import lxml.html
import scraperwiki
#f = {'start':'164'}  herkent dict class 
#print("hello")
#urllib.urlencode(f)
#print(f)
#  ophalen aantal pagina's ?
#  serialize 
# databank foto's ? 
# code lokaal mogelijk
# table opbouwen 

scraperwiki.sqlite.execute("drop table if exists 'tweedehands'")
scraperwiki.sqlite.execute("create table tweedehands( id integer primary key , fotoref varchar(50),omschrijving varchar(100));")  
print scraperwiki.sqlite.show_tables()


html = scraperwiki.scrape("http://www.2dehands.be/landbouw-tuinbouw/akkerbouw/?",params = {'start':'0'})
#print html
root = lxml.html.fromstring(html) 
#pgs = root.cssselect( )  # haal pagina's 
# aantal pagina's vinden a rel =nofollow

#print root.cssselect('a[rel="nofollow"]') 

totaal = root.cssselect('a[rel="nofollow"]')
deelstring = ''
totaalstring = ''
for   el in  totaal:
#print  lxml.html.tostring(el)
          deelstring = str(lxml.html.tostring(el))   
          totaalstring += deelstring   
#list naar  string 

print totaalstring
plaats = totaalstring.rpartition("start=")
plaatsgetal = plaats[2]
print plaatsgetal
i = 0
getal = ''
print 'testgetaldigit'  ,  plaatsgetal[i].isdigit() 
while ((plaatsgetal[i].isdigit())    and (i < 10)):      # resultaat te testen  niet als C 
#while (i < 10):  
       print plaatsgetal[i]  ,  'grootte ' 
       print i 
       print (plaatsgetal[i].isdigit() )
       getal += plaatsgetal[i]
       i = i +1
 
print getal  
   
tds = root.cssselect('.marktimg') # get all the <td> tags
teller = 1
print type(tds)
for td in tds:
    print type(td)
    regel = lxml.html.tostring(td)
    print type(regel)  
#    gegevens [0:2] = regel.split(' ')
#    print regel.split('   ')
    gegevens = regel.rpartition('alt')
    foto = gegevens[0]
    rest = gegevens[2]
    delen = rest.rpartition('title')
    beschrijving = delen[0]
    titel =  delen[2] 
    scraperwiki.sqlite.save(unique_keys=["id"],data={"id" : teller,"fotoref":foto,"omschrijving":beschrijving},table_name="tweedehands",verbose=2)    
#    print len(gegevens)
#    print foto , beschrijving , titel     
    teller = teller + 1
#    if teller > 50:
#        break 

for startteller in [ 41 , 52 ] :
      html = scraperwiki.scrape("http://www.2dehands.be/landbouw-tuinbouw/akkerbouw/?",params = {'start':'startteller'})
      root = lxml.html.fromstring(html) 
      tds = root.cssselect('.marktimg') # get all the <td> tags
#teller = 1
      for td in tds:
          regel = lxml.html.tostring(td)  
#    gegevens [0:2] = regel.split(' ')
#    print regel.split('   ')
          gegevens = regel.rpartition('alt')
          foto = gegevens[0]
          rest = gegevens[2]
          delen = rest.rpartition('title')
          beschrijving = delen[0]
          titel =  delen[2] 
          scraperwiki.sqlite.save(unique_keys=["id"],data={"id" : teller,"fotoref":foto,"omschrijving":beschrijving},table_name="tweedehands",verbose=2)    
#    print len(gegevens)
#    print foto , beschrijving , titel     
          teller = teller + 1
          if teller > 100:
               break 


#    print td.text                # just the text inside the HTML tag

 
#import urllib
import lxml.html
import scraperwiki
#f = {'start':'164'}  herkent dict class 
#print("hello")
#urllib.urlencode(f)
#print(f)
#  ophalen aantal pagina's ?
#  serialize 
# databank foto's ? 
# code lokaal mogelijk
# table opbouwen 

scraperwiki.sqlite.execute("drop table if exists 'tweedehands'")
scraperwiki.sqlite.execute("create table tweedehands( id integer primary key , fotoref varchar(50),omschrijving varchar(100));")  
print scraperwiki.sqlite.show_tables()


html = scraperwiki.scrape("http://www.2dehands.be/landbouw-tuinbouw/akkerbouw/?",params = {'start':'0'})
#print html
root = lxml.html.fromstring(html) 
#pgs = root.cssselect( )  # haal pagina's 
# aantal pagina's vinden a rel =nofollow

#print root.cssselect('a[rel="nofollow"]') 

totaal = root.cssselect('a[rel="nofollow"]')
deelstring = ''
totaalstring = ''
for   el in  totaal:
#print  lxml.html.tostring(el)
          deelstring = str(lxml.html.tostring(el))   
          totaalstring += deelstring   
#list naar  string 

print totaalstring
plaats = totaalstring.rpartition("start=")
plaatsgetal = plaats[2]
print plaatsgetal
i = 0
getal = ''
print 'testgetaldigit'  ,  plaatsgetal[i].isdigit() 
while ((plaatsgetal[i].isdigit())    and (i < 10)):      # resultaat te testen  niet als C 
#while (i < 10):  
       print plaatsgetal[i]  ,  'grootte ' 
       print i 
       print (plaatsgetal[i].isdigit() )
       getal += plaatsgetal[i]
       i = i +1
 
print getal  
   
tds = root.cssselect('.marktimg') # get all the <td> tags
teller = 1
print type(tds)
for td in tds:
    print type(td)
    regel = lxml.html.tostring(td)
    print type(regel)  
#    gegevens [0:2] = regel.split(' ')
#    print regel.split('   ')
    gegevens = regel.rpartition('alt')
    foto = gegevens[0]
    rest = gegevens[2]
    delen = rest.rpartition('title')
    beschrijving = delen[0]
    titel =  delen[2] 
    scraperwiki.sqlite.save(unique_keys=["id"],data={"id" : teller,"fotoref":foto,"omschrijving":beschrijving},table_name="tweedehands",verbose=2)    
#    print len(gegevens)
#    print foto , beschrijving , titel     
    teller = teller + 1
#    if teller > 50:
#        break 

for startteller in [ 41 , 52 ] :
      html = scraperwiki.scrape("http://www.2dehands.be/landbouw-tuinbouw/akkerbouw/?",params = {'start':'startteller'})
      root = lxml.html.fromstring(html) 
      tds = root.cssselect('.marktimg') # get all the <td> tags
#teller = 1
      for td in tds:
          regel = lxml.html.tostring(td)  
#    gegevens [0:2] = regel.split(' ')
#    print regel.split('   ')
          gegevens = regel.rpartition('alt')
          foto = gegevens[0]
          rest = gegevens[2]
          delen = rest.rpartition('title')
          beschrijving = delen[0]
          titel =  delen[2] 
          scraperwiki.sqlite.save(unique_keys=["id"],data={"id" : teller,"fotoref":foto,"omschrijving":beschrijving},table_name="tweedehands",verbose=2)    
#    print len(gegevens)
#    print foto , beschrijving , titel     
          teller = teller + 1
          if teller > 100:
               break 


#    print td.text                # just the text inside the HTML tag

 
