# coding: utf-8

require 'json'
require 'open-uri'

require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

ROOT_URL = 'http://www.waterloo.ca/'
SOURCE_URL = 'http://www.waterloo.ca/en/government/aboutmayorandcouncil.asp'

def scrape(href, data = {})
  url = ROOT_URL + href
  doc = Nokogiri::HTML(open(url))
  prefix, name, district_id = doc.at_css('#pageTitle h1').text.match(/(Coun\.|Mayor) (.+?)(?: - Ward (\d)|\z)/)[1..3]

  # Waterloo had emails until December 2012. Now, it's a form. Thanks a lot, Waterloo!
  data.merge!({
    name: name,
    url: url,
    photo_url: "http://www.city.waterloo.on.ca#{doc.at_css('#graphics1graphic')[:src]}",
    source_url: SOURCE_URL,
  })

  if prefix == 'Mayor'
    data['elected_office'] = 'Mayor'
    data['district_id'] = 0
    data['boundary_url'] = '/boundaries/census-subdivisions/3530016/'
  else
    data['elected_office'] = 'Councillor'
    data['district_id'] = district_id
  end

  ScraperWiki.save_sqlite(['district_id'], data)
end

doc = Nokogiri::HTML(open(SOURCE_URL))
scrape doc.at_css('#subNavContainer .current').next_element.at_css('a')[:href]

doc.css('#Table1table tr:gt(1)').each do |tr|
  scrape tr.at_css('td:eq(3) a')[:href], district_name: tr.at_css('td:eq(1) p').text[/- (.+)/, 1]
end
