require 'rest-open-uri'

data = {'regions' => {}, 'countries' => {}, 'states' => {}, 'cities' => {}}

# buggy ids?
@buggies = []

def do_query(query)
  url = 'http://www.couchsurfing.org/mapsurf_autofunctions.html'
  puts query
  begin
    result = open(url, :method => :post, :body => query).read
  rescue
    return nil
  end
end

# get regions
query = "autofunction=get_regions_auto&id=0"
result = do_query(query)

data_strings = result.split('#')[1..-1] # with removing 0|WORLD
data_strings.each do |data_string|
  pair = data_string.split('|')
  data['regions'][pair.first] = {'name' => pair.last}
end

# get countries
data['regions'].each_key do |region_id|
   query = "autofunction=get_countries_auto&id=#{region_id}"
   result = do_query(query)
   result.split('#').each do |data_string|
     pair = data_string.split('|')
     data['countries'][pair.first] = {'name' => pair.last}
   end if result
end

# get states
data['countries'].each_key do |country_id|
  query = "autofunction=get_states_auto&id=#{country_id}"
  result = do_query(query)
  result.split('#')[1..-1].each do |data_string| # with removing POPULAR CS CITIES
    pair = data_string.split('|')
    data['states'][pair.first] = {'name' => pair.last}
  end if result
end
 
# get cities
matcher = /(.*)\s\((\d*)\+/

data['states'].each_key do |state_id|
  query = "autofunction=get_cities_auto&id=#{state_id}"
  next if @buggies.include? query.match(/id=(\d+)$/)[1]
  result = do_query(query)
  result.split('#').each do |data_string|
    pair = data_string.split('|')
    result, name, popularity_level = pair.last.match(matcher).to_a
    data['cities'][pair.first] = {'name' => name, 'popularity_level' => popularity_level}
  end if result
end

# save data
ScraperWiki.save_metadata('data_columns', %w(id name type popularity_level))

%w(regions countries states).each do |type|
  data[type].each_pair do |id, props|
    types_map = {'regions' => 'region', 'countries' => 'country', 'states' => 'state', 'cities' => 'city'}
    record = {'id' => id, 'name' => props['name'], 'type' => types_map[type], 'popularity_level' => props['popularity_level']}
    ScraperWiki.save(['id'], record)
  end
end
require 'rest-open-uri'

data = {'regions' => {}, 'countries' => {}, 'states' => {}, 'cities' => {}}

# buggy ids?
@buggies = []

def do_query(query)
  url = 'http://www.couchsurfing.org/mapsurf_autofunctions.html'
  puts query
  begin
    result = open(url, :method => :post, :body => query).read
  rescue
    return nil
  end
end

# get regions
query = "autofunction=get_regions_auto&id=0"
result = do_query(query)

data_strings = result.split('#')[1..-1] # with removing 0|WORLD
data_strings.each do |data_string|
  pair = data_string.split('|')
  data['regions'][pair.first] = {'name' => pair.last}
end

# get countries
data['regions'].each_key do |region_id|
   query = "autofunction=get_countries_auto&id=#{region_id}"
   result = do_query(query)
   result.split('#').each do |data_string|
     pair = data_string.split('|')
     data['countries'][pair.first] = {'name' => pair.last}
   end if result
end

# get states
data['countries'].each_key do |country_id|
  query = "autofunction=get_states_auto&id=#{country_id}"
  result = do_query(query)
  result.split('#')[1..-1].each do |data_string| # with removing POPULAR CS CITIES
    pair = data_string.split('|')
    data['states'][pair.first] = {'name' => pair.last}
  end if result
end
 
# get cities
matcher = /(.*)\s\((\d*)\+/

data['states'].each_key do |state_id|
  query = "autofunction=get_cities_auto&id=#{state_id}"
  next if @buggies.include? query.match(/id=(\d+)$/)[1]
  result = do_query(query)
  result.split('#').each do |data_string|
    pair = data_string.split('|')
    result, name, popularity_level = pair.last.match(matcher).to_a
    data['cities'][pair.first] = {'name' => name, 'popularity_level' => popularity_level}
  end if result
end

# save data
ScraperWiki.save_metadata('data_columns', %w(id name type popularity_level))

%w(regions countries states).each do |type|
  data[type].each_pair do |id, props|
    types_map = {'regions' => 'region', 'countries' => 'country', 'states' => 'state', 'cities' => 'city'}
    record = {'id' => id, 'name' => props['name'], 'type' => types_map[type], 'popularity_level' => props['popularity_level']}
    ScraperWiki.save(['id'], record)
  end
end
