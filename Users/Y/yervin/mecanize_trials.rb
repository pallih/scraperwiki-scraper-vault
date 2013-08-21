require 'rubygems'
require 'mechanize'
require 'date'

agent = Mechanize.new
page = agent.get('http://www.edreams.com/flights/')
form = page.form('homeFlightsSearch')

agent.agent.http.tap { |http| http.reset http.connection_for(page.uri + form.action) }

first_possible_departure_date = Date.new(2013, 7, 23)
last_possible_departure_date = Date.new(2013, 8, 8)
departure_dates = first_possible_departure_date..last_possible_departure_date
min_trip_duration = 5
max_trip_duration = 10
trip_durations = min_trip_duration..max_trip_duration
id = 0

departure_dates.each do |ddate|
  trip_durations.each do |days|

    departure_date = ddate.strftime('%d/%m/%Y')
    return_date = (ddate + days).strftime('%d/%m/%Y')
    puts departure_date + " -> " + return_date

    form.departureLocation = 'St Petersburg'
    form.arrivalLocation = 'Brussels'
    form.departureDate = departure_date
    form.returnDate = return_date
    
    page = agent.submit(form)
    
    page.search('div.singleItineray-content-body').each do |result|
      price = result.search('div.singleItinerayPrice')[0].content[6..-1].to_f
      departure_time1 = result.search('td.segmentColumn2f')[0].content[1..-2]
      departure_time2 = result.search('td.segmentColumn2f')[1].content[1..-2]
      arrival_time1 = result.search('td.segmentColumn4f')[0].content.split('').reject do |c| 
        c == ' ' || c == "\n" || c == "\r" 
      end.join
      arrival_time2 = result.search('td.segmentColumn4f')[1].content.split('').reject do |c| 
        c == ' ' || c == "\n" || c == "\r" 
      end.join
      duration1 = result.search('td.segmentColumn7f span')[0].content[11..-24]
      duration2 = result.search('td.segmentColumn7f span')[1].content[11..-24]
      
      data = {
        id: id,
        price: price,
    
        departure_date: departure_date,
        departure_time1: departure_time1,
        arrival_time1: arrival_time1,
        duration1: duration1,
    
        arrival_date: return_date,
        departure_time2: departure_time2,
        arrival_time2: arrival_time2,
        duration2: duration2
      }
      puts data.to_json
      ScraperWiki::save_sqlite(['id'], data) 
      id = id + 1
    end
  end
endrequire 'rubygems'
require 'mechanize'
require 'date'

agent = Mechanize.new
page = agent.get('http://www.edreams.com/flights/')
form = page.form('homeFlightsSearch')

agent.agent.http.tap { |http| http.reset http.connection_for(page.uri + form.action) }

first_possible_departure_date = Date.new(2013, 7, 23)
last_possible_departure_date = Date.new(2013, 8, 8)
departure_dates = first_possible_departure_date..last_possible_departure_date
min_trip_duration = 5
max_trip_duration = 10
trip_durations = min_trip_duration..max_trip_duration
id = 0

departure_dates.each do |ddate|
  trip_durations.each do |days|

    departure_date = ddate.strftime('%d/%m/%Y')
    return_date = (ddate + days).strftime('%d/%m/%Y')
    puts departure_date + " -> " + return_date

    form.departureLocation = 'St Petersburg'
    form.arrivalLocation = 'Brussels'
    form.departureDate = departure_date
    form.returnDate = return_date
    
    page = agent.submit(form)
    
    page.search('div.singleItineray-content-body').each do |result|
      price = result.search('div.singleItinerayPrice')[0].content[6..-1].to_f
      departure_time1 = result.search('td.segmentColumn2f')[0].content[1..-2]
      departure_time2 = result.search('td.segmentColumn2f')[1].content[1..-2]
      arrival_time1 = result.search('td.segmentColumn4f')[0].content.split('').reject do |c| 
        c == ' ' || c == "\n" || c == "\r" 
      end.join
      arrival_time2 = result.search('td.segmentColumn4f')[1].content.split('').reject do |c| 
        c == ' ' || c == "\n" || c == "\r" 
      end.join
      duration1 = result.search('td.segmentColumn7f span')[0].content[11..-24]
      duration2 = result.search('td.segmentColumn7f span')[1].content[11..-24]
      
      data = {
        id: id,
        price: price,
    
        departure_date: departure_date,
        departure_time1: departure_time1,
        arrival_time1: arrival_time1,
        duration1: duration1,
    
        arrival_date: return_date,
        departure_time2: departure_time2,
        arrival_time2: arrival_time2,
        duration2: duration2
      }
      puts data.to_json
      ScraperWiki::save_sqlite(['id'], data) 
      id = id + 1
    end
  end
end