require 'net/http'
require 'csv'

require 'open-uri'
require 'nokogiri'


unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

BASE_URL = 'http://data.ottawa.ca'

doc = Nokogiri::HTML(open(BASE_URL + "/en/dataset/elected-officials-2010-2014"))
url = doc.css('#dataset-resources a').find do |a|
  a.at_css('.format-box').text == 'csv'
end[:href]
doc = Nokogiri::HTML(open(BASE_URL + url))
url = doc.at_css('.resource-actions a')['href']

CSV.parse(open(url).read, :headers => true) do |record|
  data = {
    district_name: record['District name'],
    elected_office: record['Elected office'],
    source_url: url,
    first_name: record['First name'],
    last_name: record['Last name'],
    party_name: record['Party name'],
    email: record['Email'],
    url: record['URL'],
    photo_url: record['Photo URL'],
    personal_url: record['Personal URL'],
    district_id: record['District ID'],
    gender: record['Gender'],
    offices: [{
      postal: record['Address line 1'] + ", " + record['Locality'] + " " + record['Province'] + "  " + record['Postal code'],
      tel: record['Phone'],
      fax: record['Fax']
    }].to_json
  }

  if data[:elected_office] == 'Mayor'
    data[:district_name] = ''
    data[:district_id] = ''
    data['boundary_url'] = '/boundaries/census-subdivisions/3506008/'
  end
  
  if data[:personal_url] && !data[:personal_url].include?('http://')
    data[:personal_url] = 'http://' + data[:personal_url]
  end

  ScraperWiki.save_sqlite(['district_id'], data)
end
require 'net/http'
require 'csv'

require 'open-uri'
require 'nokogiri'


unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

BASE_URL = 'http://data.ottawa.ca'

doc = Nokogiri::HTML(open(BASE_URL + "/en/dataset/elected-officials-2010-2014"))
url = doc.css('#dataset-resources a').find do |a|
  a.at_css('.format-box').text == 'csv'
end[:href]
doc = Nokogiri::HTML(open(BASE_URL + url))
url = doc.at_css('.resource-actions a')['href']

CSV.parse(open(url).read, :headers => true) do |record|
  data = {
    district_name: record['District name'],
    elected_office: record['Elected office'],
    source_url: url,
    first_name: record['First name'],
    last_name: record['Last name'],
    party_name: record['Party name'],
    email: record['Email'],
    url: record['URL'],
    photo_url: record['Photo URL'],
    personal_url: record['Personal URL'],
    district_id: record['District ID'],
    gender: record['Gender'],
    offices: [{
      postal: record['Address line 1'] + ", " + record['Locality'] + " " + record['Province'] + "  " + record['Postal code'],
      tel: record['Phone'],
      fax: record['Fax']
    }].to_json
  }

  if data[:elected_office] == 'Mayor'
    data[:district_name] = ''
    data[:district_id] = ''
    data['boundary_url'] = '/boundaries/census-subdivisions/3506008/'
  end
  
  if data[:personal_url] && !data[:personal_url].include?('http://')
    data[:personal_url] = 'http://' + data[:personal_url]
  end

  ScraperWiki.save_sqlite(['district_id'], data)
end
