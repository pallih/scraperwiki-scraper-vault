require 'rubygems'
require 'mechanize'
require 'nokogiri'
require 'open-uri'
require 'typhoeus'
require 'date'
require 'yaml'

url = 'http://ratings.food.gov.uk/advanced-search/en-GB?sm=1'

doc = Nokogiri.HTML(open(url))

options = doc.search('#ctl00_ContentPlaceHolder1_uxLocalAuthorityList').search('option')

options.each do |option|
  council = {}
  council[:name] = option.inner_text
  council[:id] = option[:value]
  ScraperWiki.save([:id], council)
end

