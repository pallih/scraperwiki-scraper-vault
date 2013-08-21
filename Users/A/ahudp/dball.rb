# encoding: utf-8
require 'mechanize'
require 'nokogiri'
require 'csv'

# SSL-Warnungen deaktivieren
I_KNOW_THAT_OPENSSL_VERIFY_PEER_EQUALS_VERIFY_NONE_IS_WRONG = nil 
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE 

BASE_URL_QUERY = "http://mobile.bahn.de/bin/mobil/query2.exe/dox?country=DEU&rt=1&use_realtime_filter=1&searchMode=NORMAL"
ABFAHRT_TAGE = [ 
  { :zeithorizont=>"1 Monat", :datum=>"04.08.2012" }
 ]
ZEIT_KORRIDOR_VON = '08:00'
ZEIT_KORRIDOR_BIS = '18:00'
MAX_VERBINDUNGEN = 4

FAHRTEN_CSV3 = 'Von;Nach
Aachen;Münster'

FAHRTEN_CSV = 'Von;Nach
Bonn;Köln
Aachen;Köln
Duisburg;Essen
Düsseldorf;Bochum
Hannover;Braunschweig
Essen;Köln
Duisburg;Düsseldorf
Dortmund;Frankfurt am Main
Lübeck;Hamburg
Kiel;Hamburg
Frankfurt am Main;Würzburg
Bremen;Hamburg
Bremen;Hannover
Hamburg;Berlin
Berlin;Leipzig
Aachen;Düsseldorf
Frankfurt am Main;Darmstadt
Mannheim;Karlsruhe
Freiburg;Karlsruhe
Stuttgart;Ulm
Bonn;Dortmund
Aachen;Dortmund
Duisburg;Dortmund
Düsseldorf;Dortmund
Hannover;Magdeburg
Bonn;Wuppertal
Aachen;Wuppertal
Essen;Frankfurt am Main
Duisburg;Köln
Dortmund;Würzburg
Lübeck;Hannover
Kiel;Hannover
Frankfurt am Main;Nürnberg
Lübeck;Berlin
Kiel;Berlin
Bremen;Berlin
Bremen;Braunschweig
Berlin;Nürnberg
Berlin;Erfurt
Aachen;Bochum
Frankfurt am Main;Mannheim
Mannheim;Stuttgart
Freiburg;Stuttgart
Stuttgart;Augsburg
Berlin;Dresden
Bonn;Bielefeld
Aachen;Bielefeld
Duisburg;Bielefeld
Düsseldorf;Bielefeld
Hannover;Berlin
Essen;Darmstadt
Duisburg;Frankfurt am Main
Dortmund;Nürnberg
Lübeck;Göttingen
Lübeck;Kassel-Wilhelmshöhe
Kiel;Kassel-Wilhelmshöhe
Kiel;Göttingen
Frankfurt am Main;Ingolstadt
Bremen;Magdeburg
Berlin;München
Berlin;Frankfurt am Main
Duisburg;Münster
Frankfurt am Main;Karlsruhe
Mannheim;Ulm
Freiburg;Ulm
Stuttgart;München
Bonn;Hannover
Aachen;Hannover
Duisburg;Hannover
Düsseldorf;Hannover
Bonn;Münster
Aachen;Münster
Essen;Mannheim
Essen;Karlsruhe
Duisburg;Würzburg
Duisburg;Nürnberg
Dortmund;München
Lübeck;Frankfurt am Main
Kiel;Frankfurt am Main
Frankfurt am Main;München
Berlin;Augsburg
Berlin;Mannheim
Duisburg;Osnabrück
Frankfurt am Main;Stuttgart
Mannheim;Augsburg
Freiburg;Augsburg
Bonn;Braunschweig
Bonn;Magdeburg
Aachen;Braunschweig
Aachen;Magdeburg
Duisburg;Braunschweig
Duisburg;Magdeburg
Düsseldorf;Braunschweig
Düsseldorf;Magdeburg
Essen;Stuttgart
Duisburg;Ingolstadt
Lübeck;Darmstadt
Lübeck;Würzburg
Kiel;Würzburg
Kiel;Darmstadt
Berlin;Karlsruhe
Bonn;Osnabrück
Aachen;Osnabrück
Duisburg;Bremen
Frankfurt am Main;Ulm
Mannheim;München
Freiburg;München
Bonn;Berlin
Aachen;Berlin
Duisburg;Berlin
Düsseldorf;Berlin
Essen;Ulm
Essen;Augsburg
Duisburg;München
Lübeck;Mannheim
Lübeck;Nürnberg
Kiel;Nürnberg
Kiel;Mannheim
Berlin;Stuttgart
Bonn;Bremen
Aachen;Bremen
Duisburg;Hamburg
Frankfurt am Main;Augsburg
Essen;München
Lübeck;Karlsruhe
Lübeck;München
Kiel;München
Kiel;Karlsruhe
Bonn;Hamburg
Aachen;Hamburg
Lübeck;Stuttgart
Kiel;Stuttgart
Lübeck;Ulm
Lübeck;Augsburg
Köln;Dortmund
Essen;Dortmund
Bochum;Dortmund
Braunschweig;Magdeburg
Köln;Wuppertal
Köln;Frankfurt am Main
Düsseldorf;Köln
Hamburg;Hannover
Würzburg;Nürnberg
Leipzig;Nürnberg
Leipzig;Erfurt
Darmstadt;Mannheim
Karlsruhe;Stuttgart
Ulm;Augsburg
Leipzig;Dresden
Köln;Bielefeld
Essen;Bielefeld
Bochum;Bielefeld
Braunschweig;Berlin
Köln;Darmstadt
Düsseldorf;Frankfurt am Main
Hamburg;Göttingen
Hamburg;Kassel-Wilhelmshöhe
Würzburg;Ingolstadt
Leipzig;München
Leipzig;Frankfurt am Main
Essen;Münster
Darmstadt;Karlsruhe
Karlsruhe;Ulm
Ulm;München
Köln;Hannover
Essen;Hannover
Bochum;Hannover
Köln;Münster
Köln;Mannheim
Köln;Karlsruhe
Düsseldorf;Würzburg
Düsseldorf;Nürnberg
Hamburg;Frankfurt am Main
Würzburg;München
Leipzig;Augsburg
Leipzig;Mannheim
Düsseldorf;Münster
Essen;Osnabrück
Darmstadt;Stuttgart
Karlsruhe;Augsburg
Köln;Braunschweig
Köln;Magdeburg
Essen;Braunschweig
Essen;Magdeburg
Bochum;Braunschweig
Bochum;Magdeburg
Köln;Stuttgart
Düsseldorf;Ingolstadt
Hamburg;Darmstadt
Hamburg;Würzburg
Leipzig;Karlsruhe
Köln;Osnabrück
Düsseldorf;Osnabrück
Essen;Bremen
Darmstadt;Ulm
Karlsruhe;München
Köln;Berlin
Essen;Berlin
Bochum;Berlin
Köln;Ulm
Köln;Augsburg
Düsseldorf;München
Hamburg;Mannheim
Hamburg;Nürnberg
Leipzig;Stuttgart
Köln;Bremen
Düsseldorf;Bremen
Essen;Hamburg
Darmstadt;Augsburg
Köln;München
Hamburg;Karlsruhe
Hamburg;München
Köln;Hamburg
Düsseldorf;Hamburg
Darmstadt;München
Hamburg;Stuttgart
Hamburg;Ulm
Hamburg;Augsburg
Dortmund;Bielefeld
Magdeburg;Berlin
Wuppertal;Dortmund
Hannover;Göttingen
Hannover;Kassel-Wilhelmshöhe
Nürnberg;Ingolstadt
Nürnberg;München
Erfurt;Frankfurt am Main
Dortmund;Münster
Augsburg;München
Dortmund;Hannover
Wuppertal;Münster
Köln;Würzburg
Köln;Nürnberg
Hannover;Frankfurt am Main
Nürnberg;Augsburg
Erfurt;Mannheim
Bochum;Münster
Dortmund;Osnabrück
Dortmund;Braunschweig
Dortmund;Magdeburg
Köln;Ingolstadt
Hannover;Darmstadt
Hannover;Würzburg
Erfurt;Karlsruhe
Wuppertal;Osnabrück
Bochum;Osnabrück
Dortmund;Bremen
Dortmund;Berlin
Hannover;Mannheim
Hannover;Nürnberg
Erfurt;Stuttgart
Wuppertal;Bremen
Bochum;Bremen
Dortmund;Hamburg
Hannover;Karlsruhe
Hannover;München
Wuppertal;Hamburg
Bochum;Hamburg
Hannover;Stuttgart
Hannover;Ulm
Hannover;Augsburg
Bielefeld;Hannover
Göttingen;Frankfurt am Main
Kassel-Wilhelmshöhe;Frankfurt am Main
Ingolstadt;München
München;Augsburg
Münster;Osnabrück
Bielefeld;Braunschweig
Bielefeld;Magdeburg
Göttingen;Darmstadt
Göttingen;Würzburg
Kassel-Wilhelmshöhe;Würzburg
Kassel-Wilhelmshöhe;Darmstadt
Münster;Bremen
Bielefeld;Berlin
Göttingen;Mannheim
Göttingen;Nürnberg
Kassel-Wilhelmshöhe;Nürnberg
Kassel-Wilhelmshöhe;Mannheim
Münster;Hamburg
Göttingen;Karlsruhe
Göttingen;München
Kassel-Wilhelmshöhe;München
Kassel-Wilhelmshöhe;Karlsruhe
Göttingen;Stuttgart
Kassel-Wilhelmshöhe;Stuttgart
Göttingen;Ulm
Göttingen;Augsburg
Osnabrück;Bremen
Osnabrück;Hamburg'

def populateRecord(von, nach, zeithorizont, datum_hinfahrt, zeit) 
  tagart = (datum_hinfahrt.wday == 0) ? "SO" : ((datum_hinfahrt.wday == 6) ? "SA" : "Wochentag")
  tage_vorher = (datum_hinfahrt - Date.today).to_i
  record = { :von=> von, :nach => nach, :datum_hinfahrt => datum_hinfahrt,
             :preis => nil, :status => 'ok', :errormessage => '', :datum_abfrage => nil,
             :tarif => "", :uhrzeit => zeit, :zeithorizont => zeithorizont, :tagart => tagart, 
             :tage_vorher => tage_vorher, :tageszeit => calcTageszeit(zeit), :verkehrsmittel => '' }
  record
end

def fahrtAbfragen(agent, von, nach, zeithorizont, datum_hinfahrt)
  p sprintf("Fahrt abfragen: %s nach %s - %s %s %s", von, nach, zeithorizont, datum_hinfahrt, ZEIT_KORRIDOR_VON)
  record = populateRecord(von, nach, zeithorizont, datum_hinfahrt, ZEIT_KORRIDOR_VON)

  begin
    # Suchseite befuellen
    suchPage = agent.post(BASE_URL_QUERY, {}, {}) 
    suchForm = suchPage.forms().first
    suchForm['REQ0JourneyStopsS0G'] = von
    suchForm['REQ0JourneyStopsZ0G'] = nach
    suchForm['REQ0JourneyDate'] = datum_hinfahrt.strftime("%d.%m.%y")
    suchForm['REQ0JourneyTime'] = ZEIT_KORRIDOR_VON 
    suchForm.checkbox_with(:name=>'REQ0HafasOptimize1').checked = true
    #suchForm.action = suchForm.action.gsub('&n=1', '&n=1')
    fahrtenPage = agent.submit(suchForm, suchForm.button_with(:name => 'start'))
    #p fahrtenPage.body
    fahrt = fahrtSuchen(fahrtenPage)
    if fahrt == nil
       record[:status] = 'Fahrt nicht gefunden'
       saveRecord(record)
    else
       record[:uhrzeit] = fahrt[:zeit]
       record[:verkehrsmittel] = fahrt[:verkehrsmittel] * ','
       # Formular mit der gesuchten Verbindung absenden
       tarifSuchen(agent, fahrt[:link], record)
    end
  rescue StandardError => error
    p "Fehler ist aufgetreten: " + error.to_s
    p error.backtrace
    record[:status] = 'Fehler'
    record[:errormessage] = error.message
    saveRecord(record)
  end
end

# Sucht im Zeitkorridor eine bzgl. der Verkehrsmittel passende Fahrt und liefert die Url fuer die Abfrage der verfuegbaren Tarife zurueck
def fahrtSuchen(fahrtenPage)
  fahrtenHtml = Nokogiri::HTML(fahrtenPage.body)
  fahrtenTable = fahrtenHtml.search('//div[@id="content"]/table')[0]
  fahrtenList = parseFahrtenTable(fahrtenPage, fahrtenTable)
  #p fahrtenList

  fahrt = findMatchingFahrt(fahrtenList, MAX_VERBINDUNGEN, ['ICE'])
  if (fahrt == nil)
    fahrt = findMatchingFahrt(fahrtenList, MAX_VERBINDUNGEN, ['ICE', 'IC'])
  end
  if (fahrt == nil)
    fahrt = findMatchingFahrt(fahrtenList, MAX_VERBINDUNGEN, ['ICE', 'IC', 'RE', 'RB'])
  end
  #p fahrt
  fahrt
end

# Parst die Tabelle mit den gefundenen Fahrten und extrahiert Links, Urzeit und Verkehrsmittel 
def parseFahrtenTable(fahrtenPage, fahrtenTable)
  result = []
  fahrtenRows = fahrtenTable.xpath('./tr')
  #p fahrtenRows
  for row in fahrtenRows do
     cells = row.xpath('./td')
     zeit = cells[0].first_element_child.inner_html.split('<')[0]
     hatPreis = cells[3].inner_html.include? ('EUR')
     # Fahrten rauslassen, die nicht im Zeitkorridor liegen 
     if zeit <= ZEIT_KORRIDOR_BIS 
       fahrt = {}
       fahrt[:zeit] = zeit
       fahrt[:link] = findZeitLink(fahrtenPage, fahrt[:zeit])
       fahrt[:verkehrsmittel] = cells[3].inner_html.split('<')[0].delete(' ').split(',')
       fahrt[:umstiege] = fahrt[:verkehrsmittel].size
       result << fahrt
     end
  end
  result
end  

def findMatchingFahrt(fahrtenList, maxUmstiege, verkehrsmittel)
  anzahlVerbindungen = 1
  result = nil
  while result == nil && anzahlVerbindungen <= maxUmstiege
    for fahrt in fahrtenList do
       if fahrt[:umstiege] = anzahlVerbindungen
          uniqVM = fahrt[:verkehrsmittel].uniq
          if (uniqVM - verkehrsmittel).size == 0
             result = fahrt
             break
          end
       end 
    end
    anzahlVerbindungen = anzahlVerbindungen + 1
  end
  result
end

def findZeitLink(fahrtenPage, zeit)
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
fahrtAbfragen(agent, "Berlin", "Dresden", "3 Monate", Date.strptime( "09.05.2012", '%d.%m.%Y'), "07:35")   
=end

fahrten = parseFahrtenCSV()
for fahrt in fahrten do
  for tag in ABFAHRT_TAGE do
    datum_hinfahrt = Date.strptime( tag[:datum], '%d.%m.%Y')
    if datum_hinfahrt > Date.today + 1 then
        fahrtAbfragen(agent, fahrt[:von], fahrt[:nach], tag[:zeithorizont], datum_hinfahrt)   
    end
  end
end
