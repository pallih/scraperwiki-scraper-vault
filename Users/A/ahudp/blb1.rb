# encoding: utf-8
require 'mechanize'
require 'nokogiri'
require 'csv'

# SSL-Warnungen deaktivieren
I_KNOW_THAT_OPENSSL_VERIFY_PEER_EQUALS_VERIFY_NONE_IS_WRONG = nil 
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE 

BASE_URL_QUERY = "http://mobile.bahn.de/bin/mobil/query2.exe/dox?country=DEU&rt=1&use_realtime_filter=1&searchMode=NORMAL"
WOCHENTAGNAMEN = ['SO', 'MO', 'DI', 'MI', 'DO', 'FR', 'SA']
ABFAHRT_TAGE = [ 
  { :zeithorizont=>"1 Monat", :datum=>"20.08.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"22.08.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"24.08.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"25.08.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"26.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"20.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"22.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"24.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"25.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"26.08.2012" }
 ]
FAHRTEN_CSV = 'Von;Nach;Zeiten Wochentags;Zeiten Samstag;Zeiten Sonntag
Hamburg;Berlin;"08:06;12:06;19:06";"08:06;12:06;19:06";"08:06;12:06;19:06"
München;Frankfurt am Main;"07:50;11:50;18:50";"07:50;11:50;18:50";"08:50;11:50;18:50"
Stuttgart;München;"07:58;11:58;18:53";"07:58;11:58;18:53";"07:58;11:58;18:53"
Berlin;Hannover;"07:48;11:48;18:49";"07:48;11:48;18:49";"07:48;11:48;18:49"
Stuttgart;Frankfurt am Main;"08:05;12:05;18:05";"08:05;12:05;18:05";"08:51;12:05;18:05"
Frankfurt am Main;Köln;"07:42;11:42;18:42";"07:42;11:42;18:42";"07:42;11:42;18:42"
Mannheim;Stuttgart;"07:53;12:30;18:39";"07:12;12:39;19:03";"07:12;12:39;18:39"
Hamburg;Bremen;"07:46;11:46;18:46";"07:46;11:46;18:46";"07:46;11:46;18:46"
Hannover;Hamburg;"07:59;11:59;19:59";"07:59;11:59;19:59";"08:20;11:59;19:59"
München;Nürnberg;"08:16;12:16;19:16";"08:16;12:16;19:16";"08:16;12:16;19:16"
München;Köln;"08:50;12:47;18:50";"07:50;12:47;18:50";"08:50;11:50;18:28"
Berlin;Leipzig;"07:52;11:52;18:51";"07:52;11:52;18:51";"07:52;11:52;18:51"
Karlsruhe;Frankfurt am Main;"09:10;11:00;19:10";"09:10;11:00;20:00";"09:10;11:00;20:00"
Magdeburg;Berlin;"08:06;12:06;19:06";"08:06;12:06;19:06";"08:06;12:06;19:06"
München;Augsburg;"08:28;11:28;18:28";"08:28;11:28;18:28";"08:28;11:28;18:28"
Ulm;München;"08:56;12:56;18:56";"08:56;12:56;18:56";"08:56;12:56;18:56"
Hamburg;Frankfurt am Main;"08:24;12:24;19:01";"08:24;12:24;19:01";"07:29;11:24;19:01"
Bielefeld;Hannover;"07:17;11:17;19:17";"07:17;11:17;19:17";"07:37;11:17;19:17"
Dresden;Leipzig;"08:23;11:53;18:53";"08:23;11:53;18:53";"08:23;11:53;18:53"
Frankfurt am Main;Berlin;"08:13;11:58;18:58";"08:13;11:58;18:58";"08:13;12:13;18:58"
Nürnberg;Frankfurt am Main;"07:29;12:00;19:00";"07:29;12:00;19:28";"08:02;12:00;19:00"
Frankfurt am Main;Hannover;"08:52;12:52;19:13";"08:52;12:52;19:13";"08:52;12:52;19:13"
Mannheim;Frankfurt am Main;"08:06;12:06;18:06";"08:06;12:06;18:06";"08:06;12:06;18:06"
Mannheim;München;"07:53;12:39;18:39";"08:39;12:39;19:32";"08:39;12:39;18:39"
Münster;Dortmund;"08:01;12:03;19:03";"08:01;12:03;19:03";"08:01;12:03;19:03"
Frankfurt am Main;Düsseldorf;"08:42;11:42;18:42";"08:42;11:42;18:42";"08:42;11:42;18:42"
Göttingen;Hannover;"08:43;11:56;18:43";"08:43;11:56;19:18";"08:56;11:56;18:22"
Berlin;Köln;"07:48;11:48;18:49";"07:48;11:48;18:49";"07:48;12:08;18:49"
Berlin;Dortmund;"07:48;11:48;18:49";"07:48;11:48;18:49";"07:48;11:48;18:49"
Karlsruhe;Mannheim;"08:00;12:00;19:01";"08:00;12:00;19:01";"08:00;12:00;19:01"
Bielefeld;Dortmund;"08:22;12:22;19:22";"08:22;12:22;19:22";"08:42;12:22;19:22"
Braunschweig;Berlin;"08:00;12:00;19:00";"08:00;12:00;19:00";"10:00;12:00;19:00"
Lübeck;Hamburg;"08:16;11:39;19:39";"08:16;11:39;19:39";"10:36;11:39;19:39"
Frankfurt am Main;Würzburg;"07:54;11:54;18:54";"07:54;11:54;19:54";"07:54;11:54;18:54"
Braunschweig;Hannover;"07:51;11:51;19:51";"07:51;11:51;19:51";"07:51;11:51;19:51"
Berlin;Bielefeld;"07:48;11:48;18:49";"07:48;11:48;18:49";"07:48;11:48;18:49"
München;Karlsruhe;"08:45;12:47;18:45";"08:45;12:47;16:48";"08:45;12:47;16:48"
Magdeburg;Hannover;"09:01;12:02;19:00";"08:02;12:02;19:00";"09:01;12:02;19:00"
Berlin;Dresden;"08:45;12:46;18:44";"08:45;12:46;18:44";"08:45;12:46;18:44"
Hamburg;München;"08:03;12:01;19:01";"08:03;12:01;19:01";"08:03;12:01;19:01"
Kiel;Hamburg;"07:53;12:38;18:38";"07:53;12:38;18:38";"07:12;12:38;18:38"
Stuttgart;Karlsruhe;"08:00;12:00;19:11";"08:00;12:00;19:11";"08:54;12:00;19:11"
Stuttgart;Augsburg;"08:53;12:53;18:53";"08:53;12:53;18:53";"08:53;12:53;18:53"
Köln;Stuttgart;"08:18;11:18;18:53";"08:18;11:18;18:53";"08:18;11:18;18:53"
Bremen;Osnabrück;"08:44;12:44;18:44";"08:44;12:44;18:44";"08:44;12:44;18:44"
Düsseldorf;München;"07:51;12:27;18:27";"07:51;12:27;18:27";"07:51;12:27;18:27"
Hannover;Bremen;"08:45;12:45;18:45";"08:45;12:45;18:45";"08:45;12:45;18:45"
München;Würzburg;"07:50;11:50;18:50";"07:50;11:50;18:50";"08:16;11:50;18:50"
Hamburg;Köln;"08:46;12:46;19:01";"08:46;12:46;19:01";"08:46;12:46;19:01"
Bremen;Berlin;"08:09;12:09;18:09";"08:09;12:09;18:09";"08:09;12:09;18:09"'

def populateRecord(von, nach, zeithorizont, datum_hinfahrt, zeit) 
  tagart = WOCHENTAGNAMEN[datum_hinfahrt.wday]
  tage_vorher = (datum_hinfahrt - Date.today).to_i
  record = { :von=> von, :nach => nach, :datum_hinfahrt => datum_hinfahrt,
             :preis => nil, :status => 'ok', :errormessage => '', :datum_abfrage => nil,
             :tarif => "", :uhrzeit => zeit, :zeithorizont => zeithorizont, :tagart => tagart, 
             :tage_vorher => tage_vorher, :tageszeit => calcTageszeit(zeit) }
  record
end

def fahrtAbfragen(agent, von, nach, zeithorizont, datum_hinfahrt, zeit)
  p sprintf("Fahrt abfragen: %s nach %s - %s %s %s", von, nach, zeithorizont, datum_hinfahrt, zeit)
  record = populateRecord(von, nach, zeithorizont, datum_hinfahrt, zeit)

  begin
    # Suchseite befuellen
    suchPage = agent.post(BASE_URL_QUERY, {}, {}) 
    suchForm = suchPage.forms().first
    suchForm['REQ0JourneyStopsS0G'] = von
    suchForm['REQ0JourneyStopsZ0G'] = nach
    suchForm['REQ0JourneyDate'] = datum_hinfahrt.strftime("%d.%m.%y")
    suchForm['REQ0JourneyTime'] = zeit
    suchForm.checkbox_with(:name=>'REQ0HafasOptimize1').checked = false
    fahrtenPage = agent.submit(suchForm, suchForm.button_with(:name => 'start'))
    fahrtLink = fahrtSuchen(fahrtenPage, zeit)
    if fahrtLink == nil
       record[:status] = 'Fahrt nicht gefunden'
       saveRecord(record)
    else
       # Formular mit der gesuchten Verbindung absenden
       tarifSuchen(agent, fahrtLink, record)
    end
  rescue StandardError => error
    p "Fehler ist aufgetreten: " + error.to_s
    p error.backtrace
    record[:status] = 'Fehler'
    record[:errormessage] = error.message
    saveRecord(record)
  end
end

# Sucht die richtige Fahrt fuer die gewuenschte Zeit und liefert die Url fuer die Abfrage der verfuegbaren Tarife zurueck
def fahrtSuchen(fahrtenPage , zeit)
  for link in fahrtenPage.links do
    if link.text().start_with? zeit
      return link
    end
  end
  nil
end
    
# Extrahiert die Preise aus der Tarifwauswahl
def tarifSuchen(agent, fahrt_link, record)  
  # Zunaechst die Seite mit den Tarifen abfragen
  tarifwahlPage = agent.click(fahrt_link)
  # p tarifwahlPage.body

  tarifwahlHtml = Nokogiri::HTML(tarifwahlPage.body)
  tarifWahlForm = tarifwahlHtml.search("//form")[0]

  tarifSpans = tarifWahlForm.xpath('./div[@class="fline"]/span')
  if tarifSpans.empty? then
     record[:status] = 'Preisauskunft nicht moeglich'
     saveRecord(record)
  else
    for tarifSpan in tarifSpans do  
      record[:status] = 'OK'
      # &nbsp werden zu utf-8 zeichen umgewandelt, das gegen Leerzeichen ersetzt werden muss
      record[:preis] = tarifSpan.text.gsub(/\302\240/," ").split(' ')[0]
      record[:tarif] = tarifSpan.parent.next_sibling.first_element_child.text.gsub(/\302\240/," ")
      saveRecord(record)
    end
  end
end

def saveRecord(record)  
  record[:datum_abfrage] = Time.new.strftime("%d.%m.%Y %H:%M:%S:%L")
  print record[:status] + ': ' 
  p record
  ScraperWiki::save_sqlite(unique_keys=["von", "nach", "datum_hinfahrt", "uhrzeit", "tarif", "datum_abfrage"], record, table_name="preise") 
end

def calcTageszeit(zeit)
  zeit < '11:00' ? 'MO' : (zeit < '16:00' ? 'MI' : 'AB')
end

def parseFahrtenCSV()
  result = CSV.parse(FAHRTEN_CSV, { :headers => true, :col_sep => ';', :header_converters => :symbol })
  result
end

agent = Mechanize.new
=begin
ScraperWiki::sqliteexecute("delete from preise where datum_abfrage like '05.07.2012 0%'")
ScraperWiki::commit
fahrtAbfragen(agent, "Berlin", "Dresden", "3 Monate", Date.strptime( "09.05.2012", '%d.%m.%Y'), "07:35")   
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
# encoding: utf-8
require 'mechanize'
require 'nokogiri'
require 'csv'

# SSL-Warnungen deaktivieren
I_KNOW_THAT_OPENSSL_VERIFY_PEER_EQUALS_VERIFY_NONE_IS_WRONG = nil 
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE 

BASE_URL_QUERY = "http://mobile.bahn.de/bin/mobil/query2.exe/dox?country=DEU&rt=1&use_realtime_filter=1&searchMode=NORMAL"
WOCHENTAGNAMEN = ['SO', 'MO', 'DI', 'MI', 'DO', 'FR', 'SA']
ABFAHRT_TAGE = [ 
  { :zeithorizont=>"1 Monat", :datum=>"20.08.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"22.08.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"24.08.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"25.08.2012" },
  { :zeithorizont=>"1 Monat", :datum=>"26.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"20.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"22.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"24.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"25.08.2012" },
  { :zeithorizont=>"3 Monate", :datum=>"26.08.2012" }
 ]
FAHRTEN_CSV = 'Von;Nach;Zeiten Wochentags;Zeiten Samstag;Zeiten Sonntag
Hamburg;Berlin;"08:06;12:06;19:06";"08:06;12:06;19:06";"08:06;12:06;19:06"
München;Frankfurt am Main;"07:50;11:50;18:50";"07:50;11:50;18:50";"08:50;11:50;18:50"
Stuttgart;München;"07:58;11:58;18:53";"07:58;11:58;18:53";"07:58;11:58;18:53"
Berlin;Hannover;"07:48;11:48;18:49";"07:48;11:48;18:49";"07:48;11:48;18:49"
Stuttgart;Frankfurt am Main;"08:05;12:05;18:05";"08:05;12:05;18:05";"08:51;12:05;18:05"
Frankfurt am Main;Köln;"07:42;11:42;18:42";"07:42;11:42;18:42";"07:42;11:42;18:42"
Mannheim;Stuttgart;"07:53;12:30;18:39";"07:12;12:39;19:03";"07:12;12:39;18:39"
Hamburg;Bremen;"07:46;11:46;18:46";"07:46;11:46;18:46";"07:46;11:46;18:46"
Hannover;Hamburg;"07:59;11:59;19:59";"07:59;11:59;19:59";"08:20;11:59;19:59"
München;Nürnberg;"08:16;12:16;19:16";"08:16;12:16;19:16";"08:16;12:16;19:16"
München;Köln;"08:50;12:47;18:50";"07:50;12:47;18:50";"08:50;11:50;18:28"
Berlin;Leipzig;"07:52;11:52;18:51";"07:52;11:52;18:51";"07:52;11:52;18:51"
Karlsruhe;Frankfurt am Main;"09:10;11:00;19:10";"09:10;11:00;20:00";"09:10;11:00;20:00"
Magdeburg;Berlin;"08:06;12:06;19:06";"08:06;12:06;19:06";"08:06;12:06;19:06"
München;Augsburg;"08:28;11:28;18:28";"08:28;11:28;18:28";"08:28;11:28;18:28"
Ulm;München;"08:56;12:56;18:56";"08:56;12:56;18:56";"08:56;12:56;18:56"
Hamburg;Frankfurt am Main;"08:24;12:24;19:01";"08:24;12:24;19:01";"07:29;11:24;19:01"
Bielefeld;Hannover;"07:17;11:17;19:17";"07:17;11:17;19:17";"07:37;11:17;19:17"
Dresden;Leipzig;"08:23;11:53;18:53";"08:23;11:53;18:53";"08:23;11:53;18:53"
Frankfurt am Main;Berlin;"08:13;11:58;18:58";"08:13;11:58;18:58";"08:13;12:13;18:58"
Nürnberg;Frankfurt am Main;"07:29;12:00;19:00";"07:29;12:00;19:28";"08:02;12:00;19:00"
Frankfurt am Main;Hannover;"08:52;12:52;19:13";"08:52;12:52;19:13";"08:52;12:52;19:13"
Mannheim;Frankfurt am Main;"08:06;12:06;18:06";"08:06;12:06;18:06";"08:06;12:06;18:06"
Mannheim;München;"07:53;12:39;18:39";"08:39;12:39;19:32";"08:39;12:39;18:39"
Münster;Dortmund;"08:01;12:03;19:03";"08:01;12:03;19:03";"08:01;12:03;19:03"
Frankfurt am Main;Düsseldorf;"08:42;11:42;18:42";"08:42;11:42;18:42";"08:42;11:42;18:42"
Göttingen;Hannover;"08:43;11:56;18:43";"08:43;11:56;19:18";"08:56;11:56;18:22"
Berlin;Köln;"07:48;11:48;18:49";"07:48;11:48;18:49";"07:48;12:08;18:49"
Berlin;Dortmund;"07:48;11:48;18:49";"07:48;11:48;18:49";"07:48;11:48;18:49"
Karlsruhe;Mannheim;"08:00;12:00;19:01";"08:00;12:00;19:01";"08:00;12:00;19:01"
Bielefeld;Dortmund;"08:22;12:22;19:22";"08:22;12:22;19:22";"08:42;12:22;19:22"
Braunschweig;Berlin;"08:00;12:00;19:00";"08:00;12:00;19:00";"10:00;12:00;19:00"
Lübeck;Hamburg;"08:16;11:39;19:39";"08:16;11:39;19:39";"10:36;11:39;19:39"
Frankfurt am Main;Würzburg;"07:54;11:54;18:54";"07:54;11:54;19:54";"07:54;11:54;18:54"
Braunschweig;Hannover;"07:51;11:51;19:51";"07:51;11:51;19:51";"07:51;11:51;19:51"
Berlin;Bielefeld;"07:48;11:48;18:49";"07:48;11:48;18:49";"07:48;11:48;18:49"
München;Karlsruhe;"08:45;12:47;18:45";"08:45;12:47;16:48";"08:45;12:47;16:48"
Magdeburg;Hannover;"09:01;12:02;19:00";"08:02;12:02;19:00";"09:01;12:02;19:00"
Berlin;Dresden;"08:45;12:46;18:44";"08:45;12:46;18:44";"08:45;12:46;18:44"
Hamburg;München;"08:03;12:01;19:01";"08:03;12:01;19:01";"08:03;12:01;19:01"
Kiel;Hamburg;"07:53;12:38;18:38";"07:53;12:38;18:38";"07:12;12:38;18:38"
Stuttgart;Karlsruhe;"08:00;12:00;19:11";"08:00;12:00;19:11";"08:54;12:00;19:11"
Stuttgart;Augsburg;"08:53;12:53;18:53";"08:53;12:53;18:53";"08:53;12:53;18:53"
Köln;Stuttgart;"08:18;11:18;18:53";"08:18;11:18;18:53";"08:18;11:18;18:53"
Bremen;Osnabrück;"08:44;12:44;18:44";"08:44;12:44;18:44";"08:44;12:44;18:44"
Düsseldorf;München;"07:51;12:27;18:27";"07:51;12:27;18:27";"07:51;12:27;18:27"
Hannover;Bremen;"08:45;12:45;18:45";"08:45;12:45;18:45";"08:45;12:45;18:45"
München;Würzburg;"07:50;11:50;18:50";"07:50;11:50;18:50";"08:16;11:50;18:50"
Hamburg;Köln;"08:46;12:46;19:01";"08:46;12:46;19:01";"08:46;12:46;19:01"
Bremen;Berlin;"08:09;12:09;18:09";"08:09;12:09;18:09";"08:09;12:09;18:09"'

def populateRecord(von, nach, zeithorizont, datum_hinfahrt, zeit) 
  tagart = WOCHENTAGNAMEN[datum_hinfahrt.wday]
  tage_vorher = (datum_hinfahrt - Date.today).to_i
  record = { :von=> von, :nach => nach, :datum_hinfahrt => datum_hinfahrt,
             :preis => nil, :status => 'ok', :errormessage => '', :datum_abfrage => nil,
             :tarif => "", :uhrzeit => zeit, :zeithorizont => zeithorizont, :tagart => tagart, 
             :tage_vorher => tage_vorher, :tageszeit => calcTageszeit(zeit) }
  record
end

def fahrtAbfragen(agent, von, nach, zeithorizont, datum_hinfahrt, zeit)
  p sprintf("Fahrt abfragen: %s nach %s - %s %s %s", von, nach, zeithorizont, datum_hinfahrt, zeit)
  record = populateRecord(von, nach, zeithorizont, datum_hinfahrt, zeit)

  begin
    # Suchseite befuellen
    suchPage = agent.post(BASE_URL_QUERY, {}, {}) 
    suchForm = suchPage.forms().first
    suchForm['REQ0JourneyStopsS0G'] = von
    suchForm['REQ0JourneyStopsZ0G'] = nach
    suchForm['REQ0JourneyDate'] = datum_hinfahrt.strftime("%d.%m.%y")
    suchForm['REQ0JourneyTime'] = zeit
    suchForm.checkbox_with(:name=>'REQ0HafasOptimize1').checked = false
    fahrtenPage = agent.submit(suchForm, suchForm.button_with(:name => 'start'))
    fahrtLink = fahrtSuchen(fahrtenPage, zeit)
    if fahrtLink == nil
       record[:status] = 'Fahrt nicht gefunden'
       saveRecord(record)
    else
       # Formular mit der gesuchten Verbindung absenden
       tarifSuchen(agent, fahrtLink, record)
    end
  rescue StandardError => error
    p "Fehler ist aufgetreten: " + error.to_s
    p error.backtrace
    record[:status] = 'Fehler'
    record[:errormessage] = error.message
    saveRecord(record)
  end
end

# Sucht die richtige Fahrt fuer die gewuenschte Zeit und liefert die Url fuer die Abfrage der verfuegbaren Tarife zurueck
def fahrtSuchen(fahrtenPage , zeit)
  for link in fahrtenPage.links do
    if link.text().start_with? zeit
      return link
    end
  end
  nil
end
    
# Extrahiert die Preise aus der Tarifwauswahl
def tarifSuchen(agent, fahrt_link, record)  
  # Zunaechst die Seite mit den Tarifen abfragen
  tarifwahlPage = agent.click(fahrt_link)
  # p tarifwahlPage.body

  tarifwahlHtml = Nokogiri::HTML(tarifwahlPage.body)
  tarifWahlForm = tarifwahlHtml.search("//form")[0]

  tarifSpans = tarifWahlForm.xpath('./div[@class="fline"]/span')
  if tarifSpans.empty? then
     record[:status] = 'Preisauskunft nicht moeglich'
     saveRecord(record)
  else
    for tarifSpan in tarifSpans do  
      record[:status] = 'OK'
      # &nbsp werden zu utf-8 zeichen umgewandelt, das gegen Leerzeichen ersetzt werden muss
      record[:preis] = tarifSpan.text.gsub(/\302\240/," ").split(' ')[0]
      record[:tarif] = tarifSpan.parent.next_sibling.first_element_child.text.gsub(/\302\240/," ")
      saveRecord(record)
    end
  end
end

def saveRecord(record)  
  record[:datum_abfrage] = Time.new.strftime("%d.%m.%Y %H:%M:%S:%L")
  print record[:status] + ': ' 
  p record
  ScraperWiki::save_sqlite(unique_keys=["von", "nach", "datum_hinfahrt", "uhrzeit", "tarif", "datum_abfrage"], record, table_name="preise") 
end

def calcTageszeit(zeit)
  zeit < '11:00' ? 'MO' : (zeit < '16:00' ? 'MI' : 'AB')
end

def parseFahrtenCSV()
  result = CSV.parse(FAHRTEN_CSV, { :headers => true, :col_sep => ';', :header_converters => :symbol })
  result
end

agent = Mechanize.new
=begin
ScraperWiki::sqliteexecute("delete from preise where datum_abfrage like '05.07.2012 0%'")
ScraperWiki::commit
fahrtAbfragen(agent, "Berlin", "Dresden", "3 Monate", Date.strptime( "09.05.2012", '%d.%m.%Y'), "07:35")   
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
