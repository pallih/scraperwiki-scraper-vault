# encoding: UTF-8

require 'uri'
require 'nokogiri'  
require 'rubygems'
require 'mechanize'

id_datum=1
id_artist=2
id_ort=3
id_preis=4
id_beschreibung=5
id_vorverkauf=6
id_buchen=7

agent = Mechanize.new
agent.get('http://www.kleinkunstbuehne-straubing.de/10596.html')
doc = agent.page.at('html/body/div/table/tr[2]/td/table/tr/td[2]/table/tr[2]/td')
puts doc
id = 0

#puts "€"

zeit=""
artist=""
ort=""
preis=""
desc=""
vvk=""
buchung=""


for part in doc.search('p')
  if part.text.strip =~ /^((Montag)|(Dienstag)|(Mittwoch)|(Donnerstag)|(Freitag)|(Samstag)|(Sonntag))\W\s[0-9]+\W[0-9]+\W[0-9]\s*\d\d/  #[0-9]+:[0-9]\sUhr
    id = 1
  elsif part.text.strip =~ /^Festhalle Leutkirch/
    id = 3
  elsif part.text.strip =~ /^Vorverk((au)|(ua))f.*€/
    id = 4
  elsif part.text.strip =~ /^Vorverkauf\W/ # nirgends euro
    id = 6
    # zufügen aber zu 6??
  elsif part.text.strip =~ /^Vorverkaufsstart/
    id = 4
  elsif part.text.strip =~ /^Kartenvorverkauf/
    id = 6
  elsif part.text.strip =~ /^Ihr\sschnellster\sWeg\szur\sEintrittskarte/
    id = 7
  elsif part.text.strip == ""
    id = 8
  elsif part.text.strip =~ /^weitere Konzerte in Vorbereitung/
    id = 8
  end
  if id == 1
#    puts "1.Zeit: " + part #.text 
    zeit = zeit + part.text + "\n"
    id+=1
  elsif id == 2
#    puts "2.Artist: "+ part
    artist = artist + part.text + "\n" 
    id+=1
  elsif id == 3
#    puts "3.Ort: "+ part
    ort = ort + part.text + "\n"
   # id+=1
  elsif id == 4
#    puts "4.Preis: "+ part
    preis = preis + part.text + "\n"
    id+=1
  elsif id == 5
#    puts "5.Beschreibung: "+ part
    desc = desc + part.text + "\n"
    id+=1
  elsif id == 6
#    puts "6.VVK: "+ part
    vvk = vvk + part.text + "\n"
    id+=1
  elsif id == 7
#    puts "7.Buchung: "+ part
    buchung += part.text + "\n"

      if  buchung =~ /____________________/
      data = {
        'ort' => ort,
        'kuenstler' => artist,
        'zeit' => zeit,
        'preis' => preis,
        'beschreibung' => desc,
        'vorverkauf' => vvk,
        'buchung' => buchung
      }
    ScraperWiki.save_sqlite(unique_keys=['ort', 'kuenstler', 'zeit'], data=data) 


    zeit=""
    artist=""
    ort=""
    preis=""
    desc=""
    vvk=""
    buchung=""
    end #if
  else
    puts part
  end
end







