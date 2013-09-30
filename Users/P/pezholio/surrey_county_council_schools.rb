require 'mechanize'
require 'nokogiri'
require 'yaml'
require 'open-uri'
require 'json'

BASE_URL = 'http://www.ofsted.gov.uk/'

def get_schools 

  url = 'http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/1/any/any/any/any/any/any/gu6%207an/20/any/0/0'
    
  agent = Mechanize.new
    
  page = agent.get(url)

  max = page.search('.pagination a').last[:href].scan(/\?page=([0-9]+)/)[0][0].to_i
  
  (0..max).each do |num|
    
    page = agent.get(url + "?page="+ num.to_s)

    schools = page.search('.resultsList li')

    schools.each do |school|
      
        details = {}
      
        link = school.search('a')[0]
      
        details[:name] = link.inner_text
        details[:url] = BASE_URL + link[:href]
        details[:address] = school.search('p')[0].inner_text
        details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0]
        details[:type] = school.inner_html.scan(/Provider type: (.+)<\/p>/)[0][0]
    
        doc = JSON.parse open("http://mapit.mysociety.org/postcode/#{details[:postcode].gsub(' ', '').upcase}.json").read rescue nil
    
        details[:easting] = doc['easting'] rescue nil
        details[:northing] = doc['northing'] rescue nil
        details[:lat] = doc['wgs84_lat'] rescue nil
        details[:lng] = doc['wgs84_lon'] rescue nil

        details[:date_scraped] = Time.now
        
        unless details[:easting].nil? 
          ScraperWiki.save([:url], details)
        else
          puts details[:postcode]
        end
    end

  end 

end

get_schoolsrequire 'mechanize'
require 'nokogiri'
require 'yaml'
require 'open-uri'
require 'json'

BASE_URL = 'http://www.ofsted.gov.uk/'

def get_schools 

  url = 'http://www.ofsted.gov.uk/inspection-reports/find-inspection-report/results/1/any/any/any/any/any/any/gu6%207an/20/any/0/0'
    
  agent = Mechanize.new
    
  page = agent.get(url)

  max = page.search('.pagination a').last[:href].scan(/\?page=([0-9]+)/)[0][0].to_i
  
  (0..max).each do |num|
    
    page = agent.get(url + "?page="+ num.to_s)

    schools = page.search('.resultsList li')

    schools.each do |school|
      
        details = {}
      
        link = school.search('a')[0]
      
        details[:name] = link.inner_text
        details[:url] = BASE_URL + link[:href]
        details[:address] = school.search('p')[0].inner_text
        details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0]
        details[:type] = school.inner_html.scan(/Provider type: (.+)<\/p>/)[0][0]
    
        doc = JSON.parse open("http://mapit.mysociety.org/postcode/#{details[:postcode].gsub(' ', '').upcase}.json").read rescue nil
    
        details[:easting] = doc['easting'] rescue nil
        details[:northing] = doc['northing'] rescue nil
        details[:lat] = doc['wgs84_lat'] rescue nil
        details[:lng] = doc['wgs84_lon'] rescue nil

        details[:date_scraped] = Time.now
        
        unless details[:easting].nil? 
          ScraperWiki.save([:url], details)
        else
          puts details[:postcode]
        end
    end

  end 

end

get_schools