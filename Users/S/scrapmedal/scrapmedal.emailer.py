import scraperwiki, re, hashlib
from BeautifulSoup import BeautifulSoup
import datetime


soup = BeautifulSoup(scraperwiki.scrape('http://www.birosagsec.webgrafika.hu/hirdetmeny/update/'))
i=-1
regexx  = re.compile("hirdetmeny_[tTfF].")
rekord = soup.findAll(attrs={"class": regexx})
print len(rekord)/5
i+=5
for row in range(0, len(rekord)/5-1):
  #print rekord[i+1].text, rekord[i+2].text, rekord[i+3].text, rekord[i+4].text, rekord[i+5].text
  sor = rekord[i+1].text, rekord[i+2].text, rekord[i+3].text, rekord[i+4].text, rekord[i+5].text
  hashedsor = hashlib.md5(str(sor).encode('utf-8'));hashedsor = hashedsor.hexdigest()
 #print hasheds
  scraperwiki.sqlite.save(unique_keys=["hashed"], data={"datum":rekord[i+1].text, "ugyszam":rekord[i+2].text, "Nev":rekord[i+3].text, "cim":rekord[i+4].text, "ok":rekord[i+5].text,"hashed":hashedsor, "scrapetime":datetime.date.today()}, table_name="hirdetmeny_backup")
  i+=5
'''
scraperwiki.sqlite.execute("UPDATE hirdetmeny SET leveve = date('now') WHERE (leveve IS null) AND (hashed NOT IN (SELECT hashed FROM hirdetmeny_temp))")
scraperwiki.sqlite.execute("INSERT INTO hirdetmeny SELECT * FROM hirdetmeny_temp where hashed NOT IN (SELECT hashed FROM hirdetmeny)")
scraperwiki.sqlite.execute("DELETE FROM hirdetmeny_temp")
scraperwiki.sqlite.commit()

'''
import scraperwiki, re, hashlib
from BeautifulSoup import BeautifulSoup
import datetime


soup = BeautifulSoup(scraperwiki.scrape('http://www.birosagsec.webgrafika.hu/hirdetmeny/update/'))
i=-1
regexx  = re.compile("hirdetmeny_[tTfF].")
rekord = soup.findAll(attrs={"class": regexx})
print len(rekord)/5
i+=5
for row in range(0, len(rekord)/5-1):
  #print rekord[i+1].text, rekord[i+2].text, rekord[i+3].text, rekord[i+4].text, rekord[i+5].text
  sor = rekord[i+1].text, rekord[i+2].text, rekord[i+3].text, rekord[i+4].text, rekord[i+5].text
  hashedsor = hashlib.md5(str(sor).encode('utf-8'));hashedsor = hashedsor.hexdigest()
 #print hasheds
  scraperwiki.sqlite.save(unique_keys=["hashed"], data={"datum":rekord[i+1].text, "ugyszam":rekord[i+2].text, "Nev":rekord[i+3].text, "cim":rekord[i+4].text, "ok":rekord[i+5].text,"hashed":hashedsor, "scrapetime":datetime.date.today()}, table_name="hirdetmeny_backup")
  i+=5
'''
scraperwiki.sqlite.execute("UPDATE hirdetmeny SET leveve = date('now') WHERE (leveve IS null) AND (hashed NOT IN (SELECT hashed FROM hirdetmeny_temp))")
scraperwiki.sqlite.execute("INSERT INTO hirdetmeny SELECT * FROM hirdetmeny_temp where hashed NOT IN (SELECT hashed FROM hirdetmeny)")
scraperwiki.sqlite.execute("DELETE FROM hirdetmeny_temp")
scraperwiki.sqlite.commit()

'''
