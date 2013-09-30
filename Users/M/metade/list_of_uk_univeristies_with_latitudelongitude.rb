require 'open-uri'
require 'json'

url = 'http://www.ucas.com/students/choosingcourses/choosinguni/map/'
html = ScraperWiki.scrape(url)

universities = {}

cur, lat, lng = nil, nil
html.split("\n").each do |line|
  if line =~ %r[array_points\[(\d+)\] = \[\];]
    cur = $1
  elsif line =~ %r[array_points\[(\d+)\]\['(\w+)'\] = '(.+)']
    id, key, value = $1, $2, $3
    universities[id] ||= {}
    universities[id][key] = value
  elsif cur and line =~ %r[var lat = parseFloat\((.+)\);]
    universities[cur]['lat'] = $1
  elsif cur and line =~ %r[var lng = parseFloat\((.+)\);]
    universities[cur]['lng'] = $1
  end
end

universities.values.each do |uni|
  ScraperWiki.save_sqlite(unique_keys=['code'], data=uni)
endrequire 'open-uri'
require 'json'

url = 'http://www.ucas.com/students/choosingcourses/choosinguni/map/'
html = ScraperWiki.scrape(url)

universities = {}

cur, lat, lng = nil, nil
html.split("\n").each do |line|
  if line =~ %r[array_points\[(\d+)\] = \[\];]
    cur = $1
  elsif line =~ %r[array_points\[(\d+)\]\['(\w+)'\] = '(.+)']
    id, key, value = $1, $2, $3
    universities[id] ||= {}
    universities[id][key] = value
  elsif cur and line =~ %r[var lat = parseFloat\((.+)\);]
    universities[cur]['lat'] = $1
  elsif cur and line =~ %r[var lng = parseFloat\((.+)\);]
    universities[cur]['lng'] = $1
  end
end

universities.values.each do |uni|
  ScraperWiki.save_sqlite(unique_keys=['code'], data=uni)
end