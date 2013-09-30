# get page with list of spaces
html = ScraperWiki.scrape("http://hackerspaces.org/wiki/List_of_Hacker_Spaces")

# create nokogiri document
require 'nokogiri'
doc = Nokogiri::HTML(html)

rows = doc.search('tr')

# remove table header
rows.shift

# extract geo data
raw_string = doc.search('script')[5].inner_text.match(/\[(\{\"lat\".*)\]/)[1]
raw_rows = raw_string.split('},{')

# prepare hash storing geo data
geo = {}

raw_rows.each do |row|
  # matches [1] = lat, [2] = lon, [3] = profile_id
  match = row.match(/\"lat\":\s(.*),\s\"lon\":\s(.*),.*wiki\/(.*?)\\/)
  geo[match[3]] = "[#{match[2]},#{match[1]}]"
end

# define structure of data
ScraperWiki.save_metadata('data_columns', ['name', 'country', 'state', 'city', 'website', 'profile_id', 'coordinates'])

# main scraping
rows.each do |row|

  # basic data from table
  record = {}
  record['name']    = row.css('td')[0].inner_text
  record['country'] = row.css('td')[1].inner_text
  record['state']  = row.css('td')[2].inner_text
  record['city']  = row.css('td')[3].inner_text
  record['website'] = row.css('td')[4].inner_text
  record['profile_id'] = row.css('td')[0].search('a')[0]['href'].sub('/wiki/','')
  record['coordinates'] = geo[record['profile_id']]

  # save the record to the datastore with 'profile_id' as a unique key
  ScraperWiki.save(['profile_id'], record)
end# get page with list of spaces
html = ScraperWiki.scrape("http://hackerspaces.org/wiki/List_of_Hacker_Spaces")

# create nokogiri document
require 'nokogiri'
doc = Nokogiri::HTML(html)

rows = doc.search('tr')

# remove table header
rows.shift

# extract geo data
raw_string = doc.search('script')[5].inner_text.match(/\[(\{\"lat\".*)\]/)[1]
raw_rows = raw_string.split('},{')

# prepare hash storing geo data
geo = {}

raw_rows.each do |row|
  # matches [1] = lat, [2] = lon, [3] = profile_id
  match = row.match(/\"lat\":\s(.*),\s\"lon\":\s(.*),.*wiki\/(.*?)\\/)
  geo[match[3]] = "[#{match[2]},#{match[1]}]"
end

# define structure of data
ScraperWiki.save_metadata('data_columns', ['name', 'country', 'state', 'city', 'website', 'profile_id', 'coordinates'])

# main scraping
rows.each do |row|

  # basic data from table
  record = {}
  record['name']    = row.css('td')[0].inner_text
  record['country'] = row.css('td')[1].inner_text
  record['state']  = row.css('td')[2].inner_text
  record['city']  = row.css('td')[3].inner_text
  record['website'] = row.css('td')[4].inner_text
  record['profile_id'] = row.css('td')[0].search('a')[0]['href'].sub('/wiki/','')
  record['coordinates'] = geo[record['profile_id']]

  # save the record to the datastore with 'profile_id' as a unique key
  ScraperWiki.save(['profile_id'], record)
end