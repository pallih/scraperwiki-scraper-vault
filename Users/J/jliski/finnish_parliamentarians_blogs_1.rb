# encoding: utf-8
require 'nokogiri'
require 'open-uri'
require 'addressable/uri'

ScraperWiki::sqliteexecute("CREATE TABLE IF NOT EXISTS blogs (party string, name string, blogs string, blog1 string, blog2 string)")

page = Nokogiri::HTML(open("http://web.eduskunta.fi/Resource.phx/eduskunta/organisaatio/kansanedustajat/blogit.htx")) 
page.css("div.news tbody tr").each do |row|
  blogit = row.css("div a").map { |link| Addressable::URI.parse(link['href']).normalize.to_s }
  #puts blogit
  data = {
    name: row.css("div strong").text.split('/')[0].chomp,
    party: row.css("div strong").text.split('/')[1].chomp,
    blogs: blogit,
    blog1: blogit[0],
    blog2: blogit[1]
  }
  #puts data.to_json
  ScraperWiki::save_sqlite(['name'], data, table_name="blogs")
end# encoding: utf-8
require 'nokogiri'
require 'open-uri'
require 'addressable/uri'

ScraperWiki::sqliteexecute("CREATE TABLE IF NOT EXISTS blogs (party string, name string, blogs string, blog1 string, blog2 string)")

page = Nokogiri::HTML(open("http://web.eduskunta.fi/Resource.phx/eduskunta/organisaatio/kansanedustajat/blogit.htx")) 
page.css("div.news tbody tr").each do |row|
  blogit = row.css("div a").map { |link| Addressable::URI.parse(link['href']).normalize.to_s }
  #puts blogit
  data = {
    name: row.css("div strong").text.split('/')[0].chomp,
    party: row.css("div strong").text.split('/')[1].chomp,
    blogs: blogit,
    blog1: blogit[0],
    blog2: blogit[1]
  }
  #puts data.to_json
  ScraperWiki::save_sqlite(['name'], data, table_name="blogs")
end