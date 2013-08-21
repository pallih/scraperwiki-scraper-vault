# coding: utf-8

require 'json'
require 'open-uri'

require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

SOURCE_URL = 'http://www.cityofkingston.ca/city-hall/city-council/mayor-and-council'

doc = Nokogiri::HTML(open(SOURCE_URL))

doc.xpath('//ul[@class="no-list no-margin"]//ul[@class="no-list no-margin"]//li/a/@href ').map(&:value).each do |url|

  doc = Nokogiri::HTML(open(url))

  contact = doc.at_xpath('//div[text()[contains(.,"Phone:")]]') 
  data = {
    name: contact.xpath('./span[1]').text.delete("\r\n").strip,
    email: contact.xpath('./a').text.strip,
    offices: [
      postal: contact.text.split("\r\n")[5].gsub(/\s{2,}/,' ').strip, 
      tel: /(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})/.match(contact).to_s     
    ],
    url: url,
    photo_url: "http://www.cityofkingston.ca#{doc.at_xpath('//img[@class="innerimage"]')[:src]}",#"http://www.cityofkingston.ca#{doc.at_css('#content img')[:src]}",
    source_url: SOURCE_URL
  }  

   
  match = doc.xpath('//div[@class="interior-page-title interior-page-title-with-tools"]/h1').text.include? "Councillor"
  if match
    dist = doc.xpath('//div[@class="journal-content-article"]/h2').text.gsub("\n"," ")
    data.merge!({
      district_name: dist.split(":")[1].strip,
      district_id: dist.match(/[0-9]{1,2}/),
      elected_office: 'Councillor',
    })
  else
    data[:offices][0][:postal] = ""
    data.merge!({
      district_name: '',
      boundary_url: '/boundaries/census-subdivisions/3510010/',
      elected_office: 'Mayor'
    })
     end
  data[:offices] = data[:offices].to_json
  ScraperWiki.save_sqlite(['district_name'], data)
end

