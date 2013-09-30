# encoding: UTF-8
# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'json'
require 'net/http'

# main hash to stock results 
bibliotecas = {}

# some global vars
total_libs = 0;
page_num_pointer = 0


# let's first pass the page to get the number of Bibliotecas of the directory
directory_url = 'http://www.conabip.gob.ar/directorio_bibliotecas_populares?page='
directory_doc = Nokogiri::HTML(open(directory_url + page_num_pointer.to_s))

directory_doc.search("div[@id='view-id-directorio_bibliotecas_populares-page_1'] div[@class='view-footer']").each do |div| 
  total_libs = /(\d+) Bibliotecas Populares./.match(div)[1].to_i
end

# we'll do a count down to know when we're done
remaining_libs = total_libs

# scrap individual libraries
while remaining_libs > 0 do

  # let's read a page from the directory
  directory_url = 'http://www.conabip.gob.ar/directorio_bibliotecas_populares?page='
  directory_doc = Nokogiri::HTML(open(directory_url + page_num_pointer.to_s))

  # each Biblioteca is wrapped by .rinterna
  directory_doc.search("div[@class='rinterna ']").each do |rinterna|
    # we'll store the data specific to a directory in that hash
    biblioteca = {}

    # our id_
    conabip_nid = 0

  rinterna.search("div").each do |div|

    # curated machine name of the field
    field_name = div['class'].gsub('views-field-', '').gsub(/-value$/, '').gsub(/^field-/, '')

    # extract the id_
    if field_name == "nid"
      div.search("a").each do |a|
        biblioteca['conabip_nid'] = a['href'].match(/\/(\d+)\?/)[1].to_i
      end
    end

    # proceed with the rest of the data
    div.search("label").each do |label|

      # we only want to parse data that is actually present
      unless label.content.nil? 
        div.search("span[@class='field-content']").each do |value|        
          clean_value = value.content
          biblioteca['conabip_' + field_name.gsub('-', '_')] = clean_value
        end
      end

    end

  end

    biblioteca['id_'] = biblioteca['conabip_title']
    biblioteca.delete('conabip_title')


    # save to DB
    if (biblioteca.has_key?('id_') and !biblioteca['id_'].nil?)

      biblioteca['id_'] = 'conabip_' + biblioteca['id_']

      # geolocation
      ubi = ''
  
      if biblioteca.has_key?('conabip_dir_num')
        ubi = biblioteca['conabip_dir_num'] + ' '
      end

      unless biblioteca['conabip_dir_calle'].match(/(\d+)$/).nil? 
        ubi = biblioteca['conabip_dir_calle'].match(/(\d+)$/)[1] + '+'
      end
      ubi = ubi + biblioteca['conabip_dir_calle'].gsub(/(\d+)$/, '').gsub('.', '+') + ', ' + biblioteca['conabip_tid'] + ', Argentina'
      ubi = ubi.gsub(' ', '+')

      geolocation_url = "http://geocoding.cloudmade.com/f1ba531b81bb4596953a0343a783bd95/geocoding/v2/find.geojs?"
      geolocation_url = geolocation_url + "query=#{ubi}&results=1&return_location=true"
      resp = Net::HTTP.get_response(URI.parse(URI.escape(geolocation_url)))
      data = resp.body
      result = JSON.parse(data)

      # get local properties
      if result['features'][0].has_key? 'properties'
        result['features'][0]['properties'].each do |prop|
          unless prop[0].match(/^osm/)
            biblioteca['osm_prop_' + prop[0]] = prop[1]
          end
        end
      end
      
      # get location information
      if result['features'][0].has_key? 'location'
        result['features'][0]['location'].each do |loc|
          biblioteca['osm_loc_' + loc[0]] = loc[1]
        end
      end

      # get coordinates
      if result['features'][0]['centroid'].has_key? 'coordinates'
        biblioteca['osm_lat'] = result['features'][0]['centroid']['coordinates'][0]
        biblioteca['osm_lon'] = result['features'][0]['centroid']['coordinates'][1]
      end
p biblioteca
      bibliotecas[ biblioteca['id_'] ] = biblioteca
      ScraperWiki::save_sqlite(['id_'], bibliotecas[biblioteca['id_']])

      # lib is done, going for the next one
      remaining_libs -= 1 # debug: remaining_libs = 0
    end

  end

  # page is over, let's parse the next one
  page_num_pointer += 1

end

p bibliotecas

# encoding: UTF-8
# Blank Ruby

require 'nokogiri'
require 'open-uri'
require 'json'
require 'net/http'

# main hash to stock results 
bibliotecas = {}

# some global vars
total_libs = 0;
page_num_pointer = 0


# let's first pass the page to get the number of Bibliotecas of the directory
directory_url = 'http://www.conabip.gob.ar/directorio_bibliotecas_populares?page='
directory_doc = Nokogiri::HTML(open(directory_url + page_num_pointer.to_s))

directory_doc.search("div[@id='view-id-directorio_bibliotecas_populares-page_1'] div[@class='view-footer']").each do |div| 
  total_libs = /(\d+) Bibliotecas Populares./.match(div)[1].to_i
end

# we'll do a count down to know when we're done
remaining_libs = total_libs

# scrap individual libraries
while remaining_libs > 0 do

  # let's read a page from the directory
  directory_url = 'http://www.conabip.gob.ar/directorio_bibliotecas_populares?page='
  directory_doc = Nokogiri::HTML(open(directory_url + page_num_pointer.to_s))

  # each Biblioteca is wrapped by .rinterna
  directory_doc.search("div[@class='rinterna ']").each do |rinterna|
    # we'll store the data specific to a directory in that hash
    biblioteca = {}

    # our id_
    conabip_nid = 0

  rinterna.search("div").each do |div|

    # curated machine name of the field
    field_name = div['class'].gsub('views-field-', '').gsub(/-value$/, '').gsub(/^field-/, '')

    # extract the id_
    if field_name == "nid"
      div.search("a").each do |a|
        biblioteca['conabip_nid'] = a['href'].match(/\/(\d+)\?/)[1].to_i
      end
    end

    # proceed with the rest of the data
    div.search("label").each do |label|

      # we only want to parse data that is actually present
      unless label.content.nil? 
        div.search("span[@class='field-content']").each do |value|        
          clean_value = value.content
          biblioteca['conabip_' + field_name.gsub('-', '_')] = clean_value
        end
      end

    end

  end

    biblioteca['id_'] = biblioteca['conabip_title']
    biblioteca.delete('conabip_title')


    # save to DB
    if (biblioteca.has_key?('id_') and !biblioteca['id_'].nil?)

      biblioteca['id_'] = 'conabip_' + biblioteca['id_']

      # geolocation
      ubi = ''
  
      if biblioteca.has_key?('conabip_dir_num')
        ubi = biblioteca['conabip_dir_num'] + ' '
      end

      unless biblioteca['conabip_dir_calle'].match(/(\d+)$/).nil? 
        ubi = biblioteca['conabip_dir_calle'].match(/(\d+)$/)[1] + '+'
      end
      ubi = ubi + biblioteca['conabip_dir_calle'].gsub(/(\d+)$/, '').gsub('.', '+') + ', ' + biblioteca['conabip_tid'] + ', Argentina'
      ubi = ubi.gsub(' ', '+')

      geolocation_url = "http://geocoding.cloudmade.com/f1ba531b81bb4596953a0343a783bd95/geocoding/v2/find.geojs?"
      geolocation_url = geolocation_url + "query=#{ubi}&results=1&return_location=true"
      resp = Net::HTTP.get_response(URI.parse(URI.escape(geolocation_url)))
      data = resp.body
      result = JSON.parse(data)

      # get local properties
      if result['features'][0].has_key? 'properties'
        result['features'][0]['properties'].each do |prop|
          unless prop[0].match(/^osm/)
            biblioteca['osm_prop_' + prop[0]] = prop[1]
          end
        end
      end
      
      # get location information
      if result['features'][0].has_key? 'location'
        result['features'][0]['location'].each do |loc|
          biblioteca['osm_loc_' + loc[0]] = loc[1]
        end
      end

      # get coordinates
      if result['features'][0]['centroid'].has_key? 'coordinates'
        biblioteca['osm_lat'] = result['features'][0]['centroid']['coordinates'][0]
        biblioteca['osm_lon'] = result['features'][0]['centroid']['coordinates'][1]
      end
p biblioteca
      bibliotecas[ biblioteca['id_'] ] = biblioteca
      ScraperWiki::save_sqlite(['id_'], bibliotecas[biblioteca['id_']])

      # lib is done, going for the next one
      remaining_libs -= 1 # debug: remaining_libs = 0
    end

  end

  # page is over, let's parse the next one
  page_num_pointer += 1

end

p bibliotecas

