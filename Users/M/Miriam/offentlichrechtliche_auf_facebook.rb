# Blank Ruby


require 'rubygems'
require 'google_spreadsheet'
require 'rfgraph'




likes = []
talking = []
name = []
title = []

  
#--------------------Auf Google Tabelle zugreifen


# Einloggen
session = GoogleSpreadsheet.login("C.Solmenhof@googlemail.com", "SO12sipa")

#-------------------IDs vom Spreadsheet "TV-Sendungen auf Facebook" auslesen, vom Worksheet "Likes" 


# Tabelle aufrufen von https://docs.google.com/spreadsheet/ccc?key=0AjA1i2niwbkwdGFNaTZBc0lwdTM2bzZMV1pHSVlpaUE#gid=0
tabelle = session.spreadsheet_by_key("0AjA1i2niwbkwdGFNaTZBc0lwdTM2bzZMV1pHSVlpaUE").worksheets[0]
tabelle_discuss = session.spreadsheet_by_key("0AjA1i2niwbkwdGFNaTZBc0lwdTM2bzZMV1pHSVlpaUE").worksheets[1]


# ID´s auslesen: Inhalt von Reihe 2 ab Spalte C . Zelle A2 wäre [2, 1]. 

for col in 6..tabelle.num_cols do      # Die funktion .num_cols kommt aus google_spreadsheet und sorgt dafür, dass alle Zelle mit Werten ausgelesen werden
  name << tabelle[2, col]
  title << tabelle[3, col]    #Hier noch die jeweiligen Titel auslesen, um sie in Datastore zu speichern
end

# Zähler i auslesen, um die Runzahlen zu bestimmen und dem Programm zu sagen, in welche Zeile es schreiben soll. Er steht in Feld 1A und wird mit jedem Run um 1 erhöht

i = tabelle[1,1].to_i                                     # to_i weil spreadsheet aus irgendeinem grund auch Zahlen als strings ausliest. Die kann man dann unten nicht addieren. So macht man ein integer draus

puts name.size  
puts tabelle_discuss.title
puts i


#---------------Mit den ID die Facebookseiten aufrufen, und Likes auslesen. Weil Facebookseiten so dynamisch sind, besser die Zahl aus dem facebook api-interface graph auslesen. Dafür gibt es eine gem namens rfgraph. 
#---------------Wird alle Seiten werden nacheinander aufgerufen, die Zahl like ausgelesen und in die liste "likes" gespeichert

y = name.size            # um die Endzahl des Loops zu bestimmen
k = 0

while k < y do 
  req = RFGraph::Request.new      # Funktion aus rfgraph aufrufen
  #puts k
  res= req.get_object("#{name[k]}")  # hier wird die graph-seite aufgerufen. In res ist jetzt die ganze graph-info
  likes << res["likes"]        # schreibt werte likes ans ende einer liste  
  talking << res["talking_about_count"]  # schreibt werte wie viele darüber sprechen in eine liste

  data = {                               # diese drei werte in ein hash packen, Datenstore von scraperwiki akzeptiert nur hash
  "Titel" => title[k],
  "Diskutieren" => talking[k],
  "Likes" => likes[k]
  }
  
  ScraperWiki.save_sqlite(unique_keys=["Titel"],data=data,table_name="TV-Sendungen")  # schreibt das ganze in den Datastore von Scraperwiki
 ScraperWiki.save_sqlite(unique_keys=["Titel"],data=data,table_name="Radio")
  k +=1            # index nimmt jeweils um 1 zu. Warum das so geschrieben wird, - - wer weiss. 
end

puts likes[0]
puts talking[0]


#-----------Likes in Google Spreadsheet schreiben. Hier wieder ein loop der bis zum Ende der Tabelle läuft

k = 0 
row = 5 + i                                                 #Erster Wert steht in Reihe 5, dann mit jedem Run eine Reihe weiter unten (i wird größer)

for col in 6..tabelle.num_cols do            #Werte werden ab Spalte 6 der Reihe nach in die Spalten geschrieben  
  tabelle[row, col] = "#{likes[k]}"    #Werte aus likes am Index k in Tabelle schreiben, in Spalte 3, reihe row. 
  k +=1
end

#---------Diskutieren darüber in google Spreadsheet schreiben. Wie oben, nur Spreadsheet 1

k = 0 
row = 5 + i      

for col in 6..tabelle_discuss.num_cols do
  tabelle_discuss[row, col] = "#{talking[k]}"
  k +=1
end

#--------Datum und Run-Nummer eintragen

tabelle[1,1] = i+1  #erhöht den Zähler in der Tabelle um eins. Das muss nur einmal gemacht werden, i bleibt im ganzen Skript gleich.

datum = Time.now
#datum_array = [i,datum,datum.month,datum.day,datum.wday]

#tabelle[5+i,1] = i   # Schreibt Run-Nummer i in Spalte A, Reihe 5 + i
tabelle[5+i,2] = datum  # Schreibt Datum in Spalte B, Reihe 5+i
tabelle[5+i,3]= datum.month #schreibt monat als zahl
tabelle[5+i,4]= datum.day  #schreibt tag
tabelle[5+i,5]= datum.wday #schreibt wochentag, von 0-7, sonntag ist 0


tabelle_discuss[5+i,1] = i   # Schreibt Run-Nummer i in Spalte A, Reihe 5 + i
tabelle_discuss[5+i,2] = datum  # Schreibt Datum in Spalte B, Reihe 5+i
tabelle_discuss[5+i,3]= datum.month #schreibt monat als zahl
tabelle_discuss[5+i,4]= datum.day  #schreibt tag
tabelle_discuss[5+i,5]= datum.wday #schreibt wochentag, von 0-7, sonntag ist 0


tabelle.save()
tabelle_discuss.save()

likes.clear              #Weil die selben Variablen für alle drei Dokumente verwendet werden. Damit dann nicht noch restzahlen drinstehen
talking.clear
name.clear
# Blank Ruby


require 'rubygems'
require 'google_spreadsheet'
require 'rfgraph'




likes = []
talking = []
name = []
title = []

  
#--------------------Auf Google Tabelle zugreifen


# Einloggen
session = GoogleSpreadsheet.login("C.Solmenhof@googlemail.com", "SO12sipa")

#-------------------IDs vom Spreadsheet "TV-Sendungen auf Facebook" auslesen, vom Worksheet "Likes" 


# Tabelle aufrufen von https://docs.google.com/spreadsheet/ccc?key=0AjA1i2niwbkwdGFNaTZBc0lwdTM2bzZMV1pHSVlpaUE#gid=0
tabelle = session.spreadsheet_by_key("0AjA1i2niwbkwdGFNaTZBc0lwdTM2bzZMV1pHSVlpaUE").worksheets[0]
tabelle_discuss = session.spreadsheet_by_key("0AjA1i2niwbkwdGFNaTZBc0lwdTM2bzZMV1pHSVlpaUE").worksheets[1]


# ID´s auslesen: Inhalt von Reihe 2 ab Spalte C . Zelle A2 wäre [2, 1]. 

for col in 6..tabelle.num_cols do      # Die funktion .num_cols kommt aus google_spreadsheet und sorgt dafür, dass alle Zelle mit Werten ausgelesen werden
  name << tabelle[2, col]
  title << tabelle[3, col]    #Hier noch die jeweiligen Titel auslesen, um sie in Datastore zu speichern
end

# Zähler i auslesen, um die Runzahlen zu bestimmen und dem Programm zu sagen, in welche Zeile es schreiben soll. Er steht in Feld 1A und wird mit jedem Run um 1 erhöht

i = tabelle[1,1].to_i                                     # to_i weil spreadsheet aus irgendeinem grund auch Zahlen als strings ausliest. Die kann man dann unten nicht addieren. So macht man ein integer draus

puts name.size  
puts tabelle_discuss.title
puts i


#---------------Mit den ID die Facebookseiten aufrufen, und Likes auslesen. Weil Facebookseiten so dynamisch sind, besser die Zahl aus dem facebook api-interface graph auslesen. Dafür gibt es eine gem namens rfgraph. 
#---------------Wird alle Seiten werden nacheinander aufgerufen, die Zahl like ausgelesen und in die liste "likes" gespeichert

y = name.size            # um die Endzahl des Loops zu bestimmen
k = 0

while k < y do 
  req = RFGraph::Request.new      # Funktion aus rfgraph aufrufen
  #puts k
  res= req.get_object("#{name[k]}")  # hier wird die graph-seite aufgerufen. In res ist jetzt die ganze graph-info
  likes << res["likes"]        # schreibt werte likes ans ende einer liste  
  talking << res["talking_about_count"]  # schreibt werte wie viele darüber sprechen in eine liste

  data = {                               # diese drei werte in ein hash packen, Datenstore von scraperwiki akzeptiert nur hash
  "Titel" => title[k],
  "Diskutieren" => talking[k],
  "Likes" => likes[k]
  }
  
  ScraperWiki.save_sqlite(unique_keys=["Titel"],data=data,table_name="TV-Sendungen")  # schreibt das ganze in den Datastore von Scraperwiki
 ScraperWiki.save_sqlite(unique_keys=["Titel"],data=data,table_name="Radio")
  k +=1            # index nimmt jeweils um 1 zu. Warum das so geschrieben wird, - - wer weiss. 
end

puts likes[0]
puts talking[0]


#-----------Likes in Google Spreadsheet schreiben. Hier wieder ein loop der bis zum Ende der Tabelle läuft

k = 0 
row = 5 + i                                                 #Erster Wert steht in Reihe 5, dann mit jedem Run eine Reihe weiter unten (i wird größer)

for col in 6..tabelle.num_cols do            #Werte werden ab Spalte 6 der Reihe nach in die Spalten geschrieben  
  tabelle[row, col] = "#{likes[k]}"    #Werte aus likes am Index k in Tabelle schreiben, in Spalte 3, reihe row. 
  k +=1
end

#---------Diskutieren darüber in google Spreadsheet schreiben. Wie oben, nur Spreadsheet 1

k = 0 
row = 5 + i      

for col in 6..tabelle_discuss.num_cols do
  tabelle_discuss[row, col] = "#{talking[k]}"
  k +=1
end

#--------Datum und Run-Nummer eintragen

tabelle[1,1] = i+1  #erhöht den Zähler in der Tabelle um eins. Das muss nur einmal gemacht werden, i bleibt im ganzen Skript gleich.

datum = Time.now
#datum_array = [i,datum,datum.month,datum.day,datum.wday]

#tabelle[5+i,1] = i   # Schreibt Run-Nummer i in Spalte A, Reihe 5 + i
tabelle[5+i,2] = datum  # Schreibt Datum in Spalte B, Reihe 5+i
tabelle[5+i,3]= datum.month #schreibt monat als zahl
tabelle[5+i,4]= datum.day  #schreibt tag
tabelle[5+i,5]= datum.wday #schreibt wochentag, von 0-7, sonntag ist 0


tabelle_discuss[5+i,1] = i   # Schreibt Run-Nummer i in Spalte A, Reihe 5 + i
tabelle_discuss[5+i,2] = datum  # Schreibt Datum in Spalte B, Reihe 5+i
tabelle_discuss[5+i,3]= datum.month #schreibt monat als zahl
tabelle_discuss[5+i,4]= datum.day  #schreibt tag
tabelle_discuss[5+i,5]= datum.wday #schreibt wochentag, von 0-7, sonntag ist 0


tabelle.save()
tabelle_discuss.save()

likes.clear              #Weil die selben Variablen für alle drei Dokumente verwendet werden. Damit dann nicht noch restzahlen drinstehen
talking.clear
name.clear
