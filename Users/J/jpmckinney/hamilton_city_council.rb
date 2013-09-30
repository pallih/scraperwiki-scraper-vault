# coding: utf-8

require 'open-uri'
require 'json'

require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

SOURCE_URL = 'http://www.hamilton.ca/YourElectedOfficials/WardCouncillors/'

doc = Nokogiri::HTML(open(SOURCE_URL))

srcs = doc.xpath('//span[@id="RadEditorPlaceHolderControl0"]//img/@src').map(&:value)

doc.xpath('//h2[text()="Contact List"]/following::table//tr[position()>1]').each_with_index do |tr,i|
  texts = tr.xpath('td').map do |td|
    td.text.strip
  end

  data = {
    name: texts[1],
    email: texts[2],
    offices: [{tel: texts[3]}].to_json,
    photo_url: "http://www.hamilton.ca#{srcs[i]}",
    source_url: SOURCE_URL,
  }

  if texts[0] == 'Mayor'
    data[:district_id] = 0
    data[:boundary_url] = '/boundaries/census-subdivisions/3525005/'
    data[:elected_office] = 'Mayor'
  else
    data[:district_id] = texts[0]
    data[:district_name] = "Ward #{texts[0]}"
    data[:elected_office] = 'Councillor'
  end
 
  ScraperWiki.save_sqlite(['district_id'], data)
end# coding: utf-8

require 'open-uri'
require 'json'

require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

SOURCE_URL = 'http://www.hamilton.ca/YourElectedOfficials/WardCouncillors/'

doc = Nokogiri::HTML(open(SOURCE_URL))

srcs = doc.xpath('//span[@id="RadEditorPlaceHolderControl0"]//img/@src').map(&:value)

doc.xpath('//h2[text()="Contact List"]/following::table//tr[position()>1]').each_with_index do |tr,i|
  texts = tr.xpath('td').map do |td|
    td.text.strip
  end

  data = {
    name: texts[1],
    email: texts[2],
    offices: [{tel: texts[3]}].to_json,
    photo_url: "http://www.hamilton.ca#{srcs[i]}",
    source_url: SOURCE_URL,
  }

  if texts[0] == 'Mayor'
    data[:district_id] = 0
    data[:boundary_url] = '/boundaries/census-subdivisions/3525005/'
    data[:elected_office] = 'Mayor'
  else
    data[:district_id] = texts[0]
    data[:district_name] = "Ward #{texts[0]}"
    data[:elected_office] = 'Councillor'
  end
 
  ScraperWiki.save_sqlite(['district_id'], data)
end