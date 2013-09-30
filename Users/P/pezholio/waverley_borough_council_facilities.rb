require 'mechanize'
require 'nokogiri'
require 'yaml'
require 'open-uri'
require 'json'

BASE_URL = 'http://www.waverley.gov.uk'

facilities = {
  'Leisure Centres' => BASE_URL + '/directory/5/sports_clubs_and_leisure/category/248',
  'Playgrounds' => BASE_URL + '/directory/5/sports_clubs_and_leisure/category/250',
}

facilities.each do |type, url|
  
  agent = Mechanize.new

  page = agent.get(url)
  
  centres = page.search('.doc_info li a')
  
  centres.each do |centre|
    details = {}
  
    details[:name] = centre.inner_text
    details[:url] = BASE_URL + centre[:href]
    details[:type] = type
  
    page = agent.get(details[:url])
  
    details_hash = page.search('.serviceDetails table tr').inject({}){|hsh,tr| 
      if tr.search('th')[0].inner_text.strip.length > 0
        hsh[tr.search('th')[0].inner_text.strip] = tr.search('td')[0].inner_text 
      else
        # Add the text to an address hash
        unless hsh['Address'].nil? 
          hsh['Address'] += ", " + tr.search('td')[0].inner_text
        else
          hsh['Address'] = tr.search('td')[0].inner_text
        end
      end ;hsh
    }
  
    details[:address] = details_hash['Address'] + " " + details_hash['Postcode']
    latlng = JSON.parse open("http://www.uk-postcodes.com/postcode/#{details_hash['Postcode'].gsub(' ', '').upcase}.json").read rescue nil
    
    unless latlng.nil? 
      details[:lat] = latlng['geo']['lat'] rescue nil
      details[:lng] = latlng['geo']['lng'] rescue nil
  
      ScraperWiki.save([:url], details)
    end
  end

end
require 'mechanize'
require 'nokogiri'
require 'yaml'
require 'open-uri'
require 'json'

BASE_URL = 'http://www.waverley.gov.uk'

facilities = {
  'Leisure Centres' => BASE_URL + '/directory/5/sports_clubs_and_leisure/category/248',
  'Playgrounds' => BASE_URL + '/directory/5/sports_clubs_and_leisure/category/250',
}

facilities.each do |type, url|
  
  agent = Mechanize.new

  page = agent.get(url)
  
  centres = page.search('.doc_info li a')
  
  centres.each do |centre|
    details = {}
  
    details[:name] = centre.inner_text
    details[:url] = BASE_URL + centre[:href]
    details[:type] = type
  
    page = agent.get(details[:url])
  
    details_hash = page.search('.serviceDetails table tr').inject({}){|hsh,tr| 
      if tr.search('th')[0].inner_text.strip.length > 0
        hsh[tr.search('th')[0].inner_text.strip] = tr.search('td')[0].inner_text 
      else
        # Add the text to an address hash
        unless hsh['Address'].nil? 
          hsh['Address'] += ", " + tr.search('td')[0].inner_text
        else
          hsh['Address'] = tr.search('td')[0].inner_text
        end
      end ;hsh
    }
  
    details[:address] = details_hash['Address'] + " " + details_hash['Postcode']
    latlng = JSON.parse open("http://www.uk-postcodes.com/postcode/#{details_hash['Postcode'].gsub(' ', '').upcase}.json").read rescue nil
    
    unless latlng.nil? 
      details[:lat] = latlng['geo']['lat'] rescue nil
      details[:lng] = latlng['geo']['lng'] rescue nil
  
      ScraperWiki.save([:url], details)
    end
  end

end
