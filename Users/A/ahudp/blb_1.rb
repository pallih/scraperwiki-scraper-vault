# ;encoding: utf-8
require 'mechanize'
require 'nokogiri'
require 'csv'

# SSL-Warnungen deaktivieren
I_KNOW_THAT_OPENSSL_VERIFY_PEER_EQUALS_VERIFY_NONE_IS_WRONG = nil 
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE 

BASE_URL_ZEITEN = "https://www.berlinlinienbus.de/zeiten.php"
BASE_URL_TARIFWAHL = "https://www.berlinlinienbus.de/tarifwahl.php"
ABFAHRT_TAGE = [ 
  { :zeithorizont=>"1 Monat", :datum=>"09.07.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"11.07.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"13.07.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"14.07.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"15.07.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"20.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"22.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"24.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"25.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"26.08.2012" }
 ]
FAHRTEN_CSV = 'Von;Nach;Zeiten Wochentags;Zeiten Samstag;Zeiten Sonntag
Berlin;Hamburg;"07:00;13:00;19:00";"07:00;13:00;19:00";"07:00;13:00;19:00"
Berlin;Leipzig;08:15;08:15;08:15
Berlin;Duesseldorf;07:30;07:30;07:30
Berlin;Hannover;"07:30;13:00;21:00";"07:30;13:00;21:00";"07:30;13:00;21:00"
Berlin;Dresden;"07:45;13:45;18:15";"07:45;13:45;18:15";"07:45;13:45;18:15"
Berlin;Muenchen;08:15;08:15;08:15
Berlin;Nuernberg;08:15;08:15;08:15
Berlin;Bielefeld;07:30;07:30;07:30
Berlin;Dortmund;07:30;07:30;07:30
Berlin;Koeln;07:30;07:30;07:30
Berlin;Bremen;08:00;08:00;09:15
Berlin;Frankfurt;07:30;07:30;07:30'
=begin
Hannover;Koeln;11:00;11:00
Muenchen;Leipzig;09:45;09:45
Muenchen;Dresden;09:45;09:45
Ulm;Dresden;08:40;08:40
Frankfurt;Magdeburg;08:00;08:00
Duesseldorf;Hannover;08:30;08:30
Duesseldorf;Magdeburg;08:30;08:30
=end

ORTE = Hash[ [ 
  ['Berlin', '00001'], 
  ['Bielefeld', '00483'], 
  ['Bremen', '00034'], 
  ['Duesseldorf', '00053'], 
  ['Dortmund', '00049'], 
  ['Dresden', '00360'], 
  ['Frankfurt', '00067'], 
  ['Hamburg', '00012'], 
  ['Hannover', '00037'], 
  ['Koeln', '00054'],
  ['Leipzig', '00335'], 
  ['Muenchen', '00087'], 
  ['Magdeburg', '00003'], 
  ['Marburg', '00512'], 
  ['Nuernberg', '00085'], 
  ['Ulm', '00302'] 
] ]

def populateRecord(von, nach, zeithorizont, datum_hinfahrt, zeit) 
  tagart = (datum_hinfahrt.wday == 0) ? "SO" : ((datum_hinfahrt.wday == 6) ? "SA" : "Wochentag")
  tage_vorher = (datum_hinfahrt - Date.today).to_i;
  record = { :von=> von, :nach => nach, :datum_hinfahrt => datum_hinfahrt,
             :preis => nil, :status => 'ok', :errormessage => '', :datum_abfrage => nil,
             :tarif => "", :uhrzeit => zeit, :zeithorizont => zeithorizont, :tagart => tagart, 
             :tage_vorher => tage_vorher, :tageszeit => calcTageszeit(zeit) }
  record
end

def calcTageszeit(zeit)
  zeit < '11:00' ? 'MO' : (zeit < '16:00' ? 'MI' : 'AB')
end

def fahrtAbfragen(agent, von, nach, zeithorizont, datum_hinfahrt, zeit)
  p sprintf("Fahrt abfragen: %s(%s) nach %s(%s) - %s %s %s", von, ORTE[von], nach, ORTE[nach], zeithorizont, datum_hinfahrt, zeit)
  record = populateRecord(von, nach, zeithorizont, datum_hinfahrt, zeit)

  # Zunaechst die Seite mit den Zeiten abfragen
  zeitenPage = agent.post(BASE_URL_ZEITEN, {'datum_hin' => datum_hinfahrt.strftime("%d.%m.%y"),
       'ort_ab' => ORTE[von], 'ort_an' => ORTE[nach], 'ticket_art' => 'EF'}, {}) 
  #p page
  begin
    fahrt_id = fahrtSuchen(zeitenPage, zeit)
    #p "Fahrt-Id : " + fahrt_id
    if fahrt_id == -1 
       record[:status] = 'Ausgebucht'
       saveRecord(record)
    elsif fahrt_id == -2 
       record[:status] = 'Fahrt nicht gefunden'
       saveRecord(record)
    else
       # Formular mit der gesuchten Verbindung absenden
       tarifSuchen(agent, fahrt_id, record)
    end
  rescue StandardError => error
    p "Fehler ist aufgetreten: " + error.to_s
    p error.backtrace
    record[:status] = 'Fehler'
    record[:errormessage] = error.message
    saveRecord(record)
  end
end

# Sucht die richtige Fahrt fuer die gewuenschte Zeit und liefert die Id zurueck anhand der die Fahrt identifiziert wird 
def fahrtSuchen(zeitenPage, zeit)
  zeit_von_id = 0
  zeitenHtml = Nokogiri::HTML(zeitenPage.body)
  zeitenAbCell = zeitenHtml.search("//form[@name='formzeit']//td[text() = 'Ab: " + zeit + "']")
  if zeitenAbCell == nil || zeitenAbCell.empty? then
    zeit_von_id = -2
  else
    zeitenAnDiv = zeitenAbCell[0].parent.parent.next_sibling
    zeitenAnFirst = zeitenAnDiv.xpath("table")[0].xpath("tr")[0].xpath("td")[0]
    if zeitenAnFirst.xpath("input").length() > 0 then
       zeit_von_id = zeitenAnFirst.xpath("input")[0]["value"];
    else 
       if zeitenAnFirst.xpath("img").length() > 0 then
         zeit_von_id = -1
       else 
         zeit_von_id = -2
       end
    end 
  end
  zeit_von_id
end
    
# Extrahiert die Preise aus der Tarifwauswahl
def tarifSuchen(agent, fahrt_id, record)  
  # Zunaechst die Seite mit den Zeiten abfragen
  tarifwahlPage = agent.post(BASE_URL_TARIFWAHL, { 'zeit_ID_hin' => fahrt_id, 'ticket_art' => 'EF'}, {}) 
  #p tarifwahlPage.body

  doc = Nokogiri::HTML(tarifwahlPage.body)
  tarifWahlTable = doc.search("//table[tr/td[text()='Personenanzahl und Tarifwahl']]")[0]

  extractAndSavePreis('Normaltarif', tarifWahlTable, 'Normal', record)
  extractAndSavePreis('AKTIONS', tarifWahlTable, 'Aktion', record)
  extractAndSavePreis('Spartarif', tarifWahlTable, 'Spar', record)
end

def extractAndSavePreis(suchtext, tarifWahlTable, tarif, record)
  record[:tarif] = tarif
  record[:preis] = '' 
  tarifRows = tarifWahlTable.xpath(".//tr[td[contains(text(),'" + suchtext + "')]]")
  #p tarifWahlTable.inner_html
  if tarifRows != nil and !tarifRows.empty? then
     priceCell = tarifRows[0].xpath('./td[position()=4]//strong')[0]
     record[:preis] = priceCell.text.split(' ')[1] .to_f
     if priceCell.parent['class'] == 'mainLight' then
        record[:status] = 'Tarif nicht buchbar'
     else
        record[:status] = 'OK'
     end
  else
     record[:status] = 'Tarif nicht buchbar'
  end
  saveRecord(record)
end

def saveRecord(record)  
  record[:datum_abfrage] = Time.new.strftime("%d.%m.%Y %H:%M:%S:%L")
  p record 
  ScraperWiki::save_sqlite(unique_keys=["von", "nach", "datum_hinfahrt", "uhrzeit", "tarif", "datum_abfrage"], record, table_name="preise") 
end

def parseFahrtenCSV()
  result = CSV.parse(FAHRTEN_CSV, { :headers => true, :col_sep => ';', :header_converters => :symbol })
  result
end

agent = Mechanize.new
=begin
fahrtAbfragen(agent, "Berlin", "Dresden", "3 Monate", Date.strptime( "26.07.2012", '%d.%m.%Y'), "07:45")   
=end
fahrten = parseFahrtenCSV()
for fahrt in fahrten do
  for tag in ABFAHRT_TAGE do
    datum_hinfahrt = Date.strptime( tag[:datum], '%d.%m.%Y')
    if datum_hinfahrt > Date.today + 1 then
      zeitenListe = nil
      if datum_hinfahrt.wday == 0 then
        zeitenListe = fahrt[:zeiten_sonntag].split(';')  
      elsif datum_hinfahrt.wday == 6 then
        zeitenListe = fahrt[:zeiten_samstag].split(';')  
      else
        zeitenListe = fahrt[:zeiten_wochentags].split(';')  
      end
      for zeit in zeitenListe do 
        fahrtAbfragen(agent, fahrt[:von], fahrt[:nach], tag[:zeithorizont], datum_hinfahrt, zeit)   
      end
    end
  end
end
# ;encoding: utf-8
require 'mechanize'
require 'nokogiri'
require 'csv'

# SSL-Warnungen deaktivieren
I_KNOW_THAT_OPENSSL_VERIFY_PEER_EQUALS_VERIFY_NONE_IS_WRONG = nil 
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE 

BASE_URL_ZEITEN = "https://www.berlinlinienbus.de/zeiten.php"
BASE_URL_TARIFWAHL = "https://www.berlinlinienbus.de/tarifwahl.php"
ABFAHRT_TAGE = [ 
  { :zeithorizont=>"1 Monat", :datum=>"09.07.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"11.07.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"13.07.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"14.07.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"15.07.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"20.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"22.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"24.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"25.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"26.08.2012" }
 ]
FAHRTEN_CSV = 'Von;Nach;Zeiten Wochentags;Zeiten Samstag;Zeiten Sonntag
Berlin;Hamburg;"07:00;13:00;19:00";"07:00;13:00;19:00";"07:00;13:00;19:00"
Berlin;Leipzig;08:15;08:15;08:15
Berlin;Duesseldorf;07:30;07:30;07:30
Berlin;Hannover;"07:30;13:00;21:00";"07:30;13:00;21:00";"07:30;13:00;21:00"
Berlin;Dresden;"07:45;13:45;18:15";"07:45;13:45;18:15";"07:45;13:45;18:15"
Berlin;Muenchen;08:15;08:15;08:15
Berlin;Nuernberg;08:15;08:15;08:15
Berlin;Bielefeld;07:30;07:30;07:30
Berlin;Dortmund;07:30;07:30;07:30
Berlin;Koeln;07:30;07:30;07:30
Berlin;Bremen;08:00;08:00;09:15
Berlin;Frankfurt;07:30;07:30;07:30'
=begin
Hannover;Koeln;11:00;11:00
Muenchen;Leipzig;09:45;09:45
Muenchen;Dresden;09:45;09:45
Ulm;Dresden;08:40;08:40
Frankfurt;Magdeburg;08:00;08:00
Duesseldorf;Hannover;08:30;08:30
Duesseldorf;Magdeburg;08:30;08:30
=end

ORTE = Hash[ [ 
  ['Berlin', '00001'], 
  ['Bielefeld', '00483'], 
  ['Bremen', '00034'], 
  ['Duesseldorf', '00053'], 
  ['Dortmund', '00049'], 
  ['Dresden', '00360'], 
  ['Frankfurt', '00067'], 
  ['Hamburg', '00012'], 
  ['Hannover', '00037'], 
  ['Koeln', '00054'],
  ['Leipzig', '00335'], 
  ['Muenchen', '00087'], 
  ['Magdeburg', '00003'], 
  ['Marburg', '00512'], 
  ['Nuernberg', '00085'], 
  ['Ulm', '00302'] 
] ]

def populateRecord(von, nach, zeithorizont, datum_hinfahrt, zeit) 
  tagart = (datum_hinfahrt.wday == 0) ? "SO" : ((datum_hinfahrt.wday == 6) ? "SA" : "Wochentag")
  tage_vorher = (datum_hinfahrt - Date.today).to_i;
  record = { :von=> von, :nach => nach, :datum_hinfahrt => datum_hinfahrt,
             :preis => nil, :status => 'ok', :errormessage => '', :datum_abfrage => nil,
             :tarif => "", :uhrzeit => zeit, :zeithorizont => zeithorizont, :tagart => tagart, 
             :tage_vorher => tage_vorher, :tageszeit => calcTageszeit(zeit) }
  record
end

def calcTageszeit(zeit)
  zeit < '11:00' ? 'MO' : (zeit < '16:00' ? 'MI' : 'AB')
end

def fahrtAbfragen(agent, von, nach, zeithorizont, datum_hinfahrt, zeit)
  p sprintf("Fahrt abfragen: %s(%s) nach %s(%s) - %s %s %s", von, ORTE[von], nach, ORTE[nach], zeithorizont, datum_hinfahrt, zeit)
  record = populateRecord(von, nach, zeithorizont, datum_hinfahrt, zeit)

  # Zunaechst die Seite mit den Zeiten abfragen
  zeitenPage = agent.post(BASE_URL_ZEITEN, {'datum_hin' => datum_hinfahrt.strftime("%d.%m.%y"),
       'ort_ab' => ORTE[von], 'ort_an' => ORTE[nach], 'ticket_art' => 'EF'}, {}) 
  #p page
  begin
    fahrt_id = fahrtSuchen(zeitenPage, zeit)
    #p "Fahrt-Id : " + fahrt_id
    if fahrt_id == -1 
       record[:status] = 'Ausgebucht'
       saveRecord(record)
    elsif fahrt_id == -2 
       record[:status] = 'Fahrt nicht gefunden'
       saveRecord(record)
    else
       # Formular mit der gesuchten Verbindung absenden
       tarifSuchen(agent, fahrt_id, record)
    end
  rescue StandardError => error
    p "Fehler ist aufgetreten: " + error.to_s
    p error.backtrace
    record[:status] = 'Fehler'
    record[:errormessage] = error.message
    saveRecord(record)
  end
end

# Sucht die richtige Fahrt fuer die gewuenschte Zeit und liefert die Id zurueck anhand der die Fahrt identifiziert wird 
def fahrtSuchen(zeitenPage, zeit)
  zeit_von_id = 0
  zeitenHtml = Nokogiri::HTML(zeitenPage.body)
  zeitenAbCell = zeitenHtml.search("//form[@name='formzeit']//td[text() = 'Ab: " + zeit + "']")
  if zeitenAbCell == nil || zeitenAbCell.empty? then
    zeit_von_id = -2
  else
    zeitenAnDiv = zeitenAbCell[0].parent.parent.next_sibling
    zeitenAnFirst = zeitenAnDiv.xpath("table")[0].xpath("tr")[0].xpath("td")[0]
    if zeitenAnFirst.xpath("input").length() > 0 then
       zeit_von_id = zeitenAnFirst.xpath("input")[0]["value"];
    else 
       if zeitenAnFirst.xpath("img").length() > 0 then
         zeit_von_id = -1
       else 
         zeit_von_id = -2
       end
    end 
  end
  zeit_von_id
end
    
# Extrahiert die Preise aus der Tarifwauswahl
def tarifSuchen(agent, fahrt_id, record)  
  # Zunaechst die Seite mit den Zeiten abfragen
  tarifwahlPage = agent.post(BASE_URL_TARIFWAHL, { 'zeit_ID_hin' => fahrt_id, 'ticket_art' => 'EF'}, {}) 
  #p tarifwahlPage.body

  doc = Nokogiri::HTML(tarifwahlPage.body)
  tarifWahlTable = doc.search("//table[tr/td[text()='Personenanzahl und Tarifwahl']]")[0]

  extractAndSavePreis('Normaltarif', tarifWahlTable, 'Normal', record)
  extractAndSavePreis('AKTIONS', tarifWahlTable, 'Aktion', record)
  extractAndSavePreis('Spartarif', tarifWahlTable, 'Spar', record)
end

def extractAndSavePreis(suchtext, tarifWahlTable, tarif, record)
  record[:tarif] = tarif
  record[:preis] = '' 
  tarifRows = tarifWahlTable.xpath(".//tr[td[contains(text(),'" + suchtext + "')]]")
  #p tarifWahlTable.inner_html
  if tarifRows != nil and !tarifRows.empty? then
     priceCell = tarifRows[0].xpath('./td[position()=4]//strong')[0]
     record[:preis] = priceCell.text.split(' ')[1] .to_f
     if priceCell.parent['class'] == 'mainLight' then
        record[:status] = 'Tarif nicht buchbar'
     else
        record[:status] = 'OK'
     end
  else
     record[:status] = 'Tarif nicht buchbar'
  end
  saveRecord(record)
end

def saveRecord(record)  
  record[:datum_abfrage] = Time.new.strftime("%d.%m.%Y %H:%M:%S:%L")
  p record 
  ScraperWiki::save_sqlite(unique_keys=["von", "nach", "datum_hinfahrt", "uhrzeit", "tarif", "datum_abfrage"], record, table_name="preise") 
end

def parseFahrtenCSV()
  result = CSV.parse(FAHRTEN_CSV, { :headers => true, :col_sep => ';', :header_converters => :symbol })
  result
end

agent = Mechanize.new
=begin
fahrtAbfragen(agent, "Berlin", "Dresden", "3 Monate", Date.strptime( "26.07.2012", '%d.%m.%Y'), "07:45")   
=end
fahrten = parseFahrtenCSV()
for fahrt in fahrten do
  for tag in ABFAHRT_TAGE do
    datum_hinfahrt = Date.strptime( tag[:datum], '%d.%m.%Y')
    if datum_hinfahrt > Date.today + 1 then
      zeitenListe = nil
      if datum_hinfahrt.wday == 0 then
        zeitenListe = fahrt[:zeiten_sonntag].split(';')  
      elsif datum_hinfahrt.wday == 6 then
        zeitenListe = fahrt[:zeiten_samstag].split(';')  
      else
        zeitenListe = fahrt[:zeiten_wochentags].split(';')  
      end
      for zeit in zeitenListe do 
        fahrtAbfragen(agent, fahrt[:von], fahrt[:nach], tag[:zeithorizont], datum_hinfahrt, zeit)   
      end
    end
  end
end
