# encoding: utf-8

require 'json'

# ENV['TZ'] = 'Pacific/Auckland'

@sensors = [
  {did: 1, field: 'temperature', name: 'Temperature', unit: '°C'},
  {did: 10, field: 'ph', name: 'pH'},
  {did: 20, field: 'depth', name: 'Depth', unit: 'mm'},
  {did: 30, field: 'turbidity', name: 'Turbidity', unit: 'NTU'},
  {did: 40, field: 'conductance', name: 'Conductance', unit: 'µS/cm'},
  {did: 50, field: 'dissolved_oxygen', name: 'Dissolved oxygen', unit: '% Sat'},
]

@base_url = 'http://www.indigosystems.net.nz/webdemo/uoc2/php/database.php'
@interval = (Time.now - 48*3600)..(Time.now)

def request_data(params)
  data = ScraperWiki.scrape(@base_url, params)
  JSON.parse(data[1..-2])
end

def fetch_devices
  data = request_data(task: 'SETUP_DEVICE')
  data['devices'].collect do |device|
    {did: device['did'].to_i,
      type: device['type'].to_i,
      description: device['description'],
      lat: device['lat'].to_f,
      lng: device['lng'].to_f}
  end
end

def fetch_graph(did, interval)
  data = request_data(task: 'GRAPH', did: did, start: interval.first.to_i, end: interval.last.to_i)
  return nil if data['graph'].length < 1
  data['graph'].collect do |point|
    {time: Time.parse(point['x']), value: point['y'].to_f}
  end
end

def combine_graphs(sensors, interval)
  combined = Hash.new
  sensors.each do |sensor|
    puts "Downloading data for #{sensor[:name]}..."
    graph = fetch_graph(sensor[:did], interval)
    next if graph.nil? 
    graph.each do |point|
      combined[point[:time]] ||= Hash.new
      combined[point[:time]][sensor[:field]] = point[:value]
    end
  end
  combined
end

combined = combine_graphs(@sensors, @interval)

puts "Saving data..."
combined.each do |time, values|
  values['time'] = time
  ScraperWiki.save_sqlite(['time'], values, 'okeover_engineering_bridge')
end