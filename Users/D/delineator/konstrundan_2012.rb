# encoding: utf-8
require 'open-uri'
require 'nokogiri'
require 'uri'
require 'iconv'
require 'json'

def fix content
  Iconv.conv('utf-8//IGNORE', 'utf-8', content)
end

def location map_uri
  id = map_uri.split('/').last
  puts id
  json = open("http://map01.eniro.no/mapstate/get?id=#{id}").read
  puts json

  geocode = JSON.parse(json)
  if geocode['map']
    box = geocode['map']['bbox']
    lat = (box['top'].to_f + box['bottom'].to_f) / 2
    lon = (box['left'].to_f + box['right'].to_f) / 2
  else
    puts '==='
    puts 'not found ' + address
    puts '==='
  end
 
  return [lon, lat]
end

def store_item(doc, uri, name, parts)
  types = parts.last.split(',').map {|x| fix(x.strip.downcase) }

  types_hash = types.inject({}) {|hash, type| hash[type] = true; hash}

  map_uri = doc.at('html body table tr td p.style11').at('a') ? fix(doc.at('html body table tr td p.style11').at('a')['href']) : ''
  addresses = doc.search('html body table tr td p.style12')
  address_1 = addresses.first ? fix(addresses.first.inner_text) : ''
  address_2 = addresses.last ? fix(addresses.last.inner_text) : ''

  address_2 = '' if (address_1 == address_2)

  image_uri = if img = doc.at('img')
    puts img['src']
    URI.parse(uri).merge(img['src'])
  end

  begin
    lon, lat = location(map_uri)
  
    record = {
      'uri' => fix(uri),
      'name' => fix(name)
    }.merge(types_hash).merge({
      'address_1' => address_1,
      'address_2' => address_2,
      'map_uri' => map_uri,
      'image_uri' => image_uri,
      'longitude' => lon,
      'latitude' => lat
    })

    ScraperWiki.save_sqlite(['uri'], record, 'deltagare')
  rescue Exception => e
    puts '==='
    puts name
    puts e.to_s
    puts '==='
  end
end

def handle_item(doc, uri, name)
  if doc.at('h3')
    puts uri
    description = doc.at('h3').inner_text
    parts = description.split('•')
    
    store_item(doc, uri, name, parts) if parts.size == 2
  end
end

def run
  index_uri = 'http://konstrundan.nu/Konstrundan/html/left2.htm'
  base = URI.parse(index_uri)

  html = open(index_uri).read.force_encoding("UTF-8") 
  doc = Nokogiri::HTML html
  
  doc.search('a').each do |link|
  
    uri = base.merge(link['href']).to_s
    name = link.inner_text.to_s
  
    item = Nokogiri::HTML open(uri).read.force_encoding("UTF-8")
  
    handle_item(item, uri, name)
  end
end

run
# encoding: utf-8
require 'open-uri'
require 'nokogiri'
require 'uri'
require 'iconv'
require 'json'

def fix content
  Iconv.conv('utf-8//IGNORE', 'utf-8', content)
end

def location map_uri
  id = map_uri.split('/').last
  puts id
  json = open("http://map01.eniro.no/mapstate/get?id=#{id}").read
  puts json

  geocode = JSON.parse(json)
  if geocode['map']
    box = geocode['map']['bbox']
    lat = (box['top'].to_f + box['bottom'].to_f) / 2
    lon = (box['left'].to_f + box['right'].to_f) / 2
  else
    puts '==='
    puts 'not found ' + address
    puts '==='
  end
 
  return [lon, lat]
end

def store_item(doc, uri, name, parts)
  types = parts.last.split(',').map {|x| fix(x.strip.downcase) }

  types_hash = types.inject({}) {|hash, type| hash[type] = true; hash}

  map_uri = doc.at('html body table tr td p.style11').at('a') ? fix(doc.at('html body table tr td p.style11').at('a')['href']) : ''
  addresses = doc.search('html body table tr td p.style12')
  address_1 = addresses.first ? fix(addresses.first.inner_text) : ''
  address_2 = addresses.last ? fix(addresses.last.inner_text) : ''

  address_2 = '' if (address_1 == address_2)

  image_uri = if img = doc.at('img')
    puts img['src']
    URI.parse(uri).merge(img['src'])
  end

  begin
    lon, lat = location(map_uri)
  
    record = {
      'uri' => fix(uri),
      'name' => fix(name)
    }.merge(types_hash).merge({
      'address_1' => address_1,
      'address_2' => address_2,
      'map_uri' => map_uri,
      'image_uri' => image_uri,
      'longitude' => lon,
      'latitude' => lat
    })

    ScraperWiki.save_sqlite(['uri'], record, 'deltagare')
  rescue Exception => e
    puts '==='
    puts name
    puts e.to_s
    puts '==='
  end
end

def handle_item(doc, uri, name)
  if doc.at('h3')
    puts uri
    description = doc.at('h3').inner_text
    parts = description.split('•')
    
    store_item(doc, uri, name, parts) if parts.size == 2
  end
end

def run
  index_uri = 'http://konstrundan.nu/Konstrundan/html/left2.htm'
  base = URI.parse(index_uri)

  html = open(index_uri).read.force_encoding("UTF-8") 
  doc = Nokogiri::HTML html
  
  doc.search('a').each do |link|
  
    uri = base.merge(link['href']).to_s
    name = link.inner_text.to_s
  
    item = Nokogiri::HTML open(uri).read.force_encoding("UTF-8")
  
    handle_item(item, uri, name)
  end
end

run
