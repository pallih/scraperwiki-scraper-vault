# encoding: utf-8
require 'mechanize'
require 'nokogiri'
require 'csv'
require 'json'

# SSL-Warnungen deaktivieren
I_KNOW_THAT_OPENSSL_VERIFY_PEER_EQUALS_VERIFY_NONE_IS_WRONG = nil 
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE 

FAHRTEN_CSV = 'Von;Nach
Charles-de-Gaulle-Strasse 20, 53113 Gronau;Bergisch Gladbach'
#Bonn;Berlin'

def populateRecord(von, nach, datum_hinfahrt) 
  tagart = (datum_hinfahrt.wday == 0) ? "SO" : ((datum_hinfahrt.wday == 6) ? "SA" : "Wochentag")
  record = { :von=> von, :nach => nach, 
             :datum_abfrage => datum_hinfahrt.strftime("%d.%m.%Y %H:%M:%S:%L") ,
             :dauer_netto => nil, :dauer_mit_verkehr => nil, :distanz => nil,
             :status => 'ok', :errormessage => '', 
             :tagart => tagart}
  record
end

def fahrtAbfragen(agent, von, nach)
  p sprintf("Fahrt abfragen: %s nach %s", von, nach)
  record = populateRecord(von, nach, Time.new)

  begin
    map_key = ""
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {}
    params["origin"] = von
    params["destination"] = nach
    params[:sensor] = "false"
    params[:mode] = "driving"
    params["departure_time"] = (Time.new + (30*1/3600/24)).utc
    #params[:key] = map_key
    p "Before GET"
    serviceResult = agent.get(url, params) 
    #serviceResult = agent.get("http://maps.googleapis.com/maps/api/directions/json?origin=Boston,MA&destination=Concord,MA&waypoints=Charlestown,MA|Lexington,MA&sensor=false")
    p serviceResult.body
    
    parsedResult = JSON.parse(serviceResult.body)
    p parsedResult
    if parsedResult['status'] == 'OK' 
      duration = parsedResult['routes'][0]['legs'][0]['duration']['value'].to_i / 60
      distance = parsedResult['routes'][0]['legs'][0]['distance']['value'].to_i 
      if parsedResult['routes'][0]['legs'][0]['duration_in_traffic'] != nil 
        durationInTraffic = parsedResult['routes'][0]['legs'][0]['duration_in_traffic']['value'].to_i / 60
      else
        durationInTraffic = nil
      end
      p duration
      p durationInTraffic
      p distance

      record[:dauer_netto] = duration
      record[:distanz] = distance
      record[:dauer_mit_verkehr] = durationInTraffic
      saveRecord(record)
    end
  rescue StandardError => error
    p "Fehler ist aufgetreten: " + error.to_s
    p error.backtrace
    record[:status] = 'Fehler'
    record[:errormessage] = error.message
    saveRecord(record)
  end
end

def saveRecord(record)  
  print record[:status] + ': ' 
  p record
  ScraperWiki::save_sqlite(unique_keys=["von", "nach", "datum_abfrage"], record, table_name="routen_dauer") 
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
  fahrtAbfragen(agent, fahrt[:von], fahrt[:nach])   
end
