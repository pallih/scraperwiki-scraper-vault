# Testing simple parsing of radiation data in Finland
require 'nokogiri'
require 'open-uri'

def add_station_data
  #ScraperWiki.sqlitecommand("execute", "drop table stations")

  # Insert station data
  q = "FI-Ivalo,68.656667, 27.54
  FI-Rovaniemi,66.501389, 25.734722
  FI-Kajaani,64.225, 27.733333
  FI-Kuopio,62.8925, 27.678333
  FI-Seinäjoki,62.790278, 22.840278
  FI-Kotka,60.467306, 26.945833
  FI-Rauma,61.129167, 21.505556
  FI-Loviisa,60.456944, 26.225
  FI-Helsinki,60.170833, 24.9375"

  for row in q.split(/\n/)
    data = row.split(/,/)
    ScraperWiki.save_sqlite(['id'], { 'id' => data[0].strip, 'lat' => data[1].strip.to_f, 'lng' => data[2].strip.to_f }, "stations")
  end
end

add_station_data

# ScraperWiki.sqlitecommand("execute", "drop table measurements")

# STYK text-tv parser
doc = open('http://www.yle.fi/tekstitv/txt/P867_02.html').read
for p in doc.scan(/(\w+)\s+([\d]+,[\d]+) mikroSv\/h/)
  measurement = {}
  measurement['station_id'] = 'FI-' + p[0]
  measurement['time'] = DateTime.now.new_offset(0) # Current time in UTC
  measurement['radiation'] = p[1].gsub(",", ".").to_f * 1e-6 # Convert to Sv/h
  ScraperWiki.save_sqlite(['station_id', 'time'], measurement, 'measurements')
end# Testing simple parsing of radiation data in Finland
require 'nokogiri'
require 'open-uri'

def add_station_data
  #ScraperWiki.sqlitecommand("execute", "drop table stations")

  # Insert station data
  q = "FI-Ivalo,68.656667, 27.54
  FI-Rovaniemi,66.501389, 25.734722
  FI-Kajaani,64.225, 27.733333
  FI-Kuopio,62.8925, 27.678333
  FI-Seinäjoki,62.790278, 22.840278
  FI-Kotka,60.467306, 26.945833
  FI-Rauma,61.129167, 21.505556
  FI-Loviisa,60.456944, 26.225
  FI-Helsinki,60.170833, 24.9375"

  for row in q.split(/\n/)
    data = row.split(/,/)
    ScraperWiki.save_sqlite(['id'], { 'id' => data[0].strip, 'lat' => data[1].strip.to_f, 'lng' => data[2].strip.to_f }, "stations")
  end
end

add_station_data

# ScraperWiki.sqlitecommand("execute", "drop table measurements")

# STYK text-tv parser
doc = open('http://www.yle.fi/tekstitv/txt/P867_02.html').read
for p in doc.scan(/(\w+)\s+([\d]+,[\d]+) mikroSv\/h/)
  measurement = {}
  measurement['station_id'] = 'FI-' + p[0]
  measurement['time'] = DateTime.now.new_offset(0) # Current time in UTC
  measurement['radiation'] = p[1].gsub(",", ".").to_f * 1e-6 # Convert to Sv/h
  ScraperWiki.save_sqlite(['station_id', 'time'], measurement, 'measurements')
end