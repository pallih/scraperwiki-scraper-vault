import scraperwiki
import lxml.html
import datetime

# Blank Python

def parseTime(timeStr):
   timeStr=timeStr.replace("*","")
   timeStr=timeStr.strip()
   return datetime.datetime.strptime(timeStr, '%H.%M').time()   

urls ={"Houtzagerij" : "http://www.denhaag.nl/home/bewoners/to/Openingstijden-zwembad-de-Houtzagerij.htm",
      "Overbosch" : "http://www.denhaag.nl/home/bewoners/sport/to/Openingstijden-zwembad-Overbosch.htm",
      "Zuiderpark" : "http://www.denhaag.nl/home/bewoners/sport/to/Openingstijden-zwembad-Zuiderpark.htm",
      "Hofbad" : "http://www.denhaag.nl/home/bewoners/sport/to/Openingstijden-zwembad-het-Hofbad.htm",
      "Waterthor" : "http://www.denhaag.nl/home/bewoners/sport/to/Openingstijden-zwembad-de-Waterthor-1.htm",
      "Blinkerd"  : "http://www.denhaag.nl/home/bewoners/sport/to/Openingstijden-zwembad-de-Blinkerd.htm"
     }

vrijZwemmenTable={"Houtzagerij" : "Vrij zwemmen",
      "Overbosch" :"Vrij zwemmen tijden",
      "Zuiderpark" : "Vrij zwemmen",
      "Hofbad" : "Vrij zwemmen",
      "Waterthor" : "Vrij zwemmen",
      "Blinkerd" : "Vrij zwemmen"
 }

for zwembad in urls.keys():
    html = scraperwiki.scrape(urls[zwembad])
    root = lxml.html.fromstring(html)
    
    for el in root.cssselect("table[summary='"+vrijZwemmenTable[zwembad]+"']"):
      rows=el.cssselect("tbody tr")
      currentDay="";
      for row in rows:
        tds=row.cssselect("td")
        if (len(tds[0].text)>1):
           currentDay=tds[0].text.strip()
        if (len(tds) == 4 ):  #De Blinkerd
          leeftijd=tds[3].text
          baden="" 
        else:
          leeftijd=tds[3].text #Rest
          baden=tds[4].text 
        van=parseTime(tds[1].text);
        tot=parseTime(tds[2].text);
        data = { 'zwembad' : zwembad, 
        'dag' : currentDay, 'van' : van , 'tot' : tot, 'leeftijd' : leeftijd, 'baden' : baden  }
        scraperwiki.sqlite.save(unique_keys=[],data=data)
