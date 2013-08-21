# Blank Ruby

require 'net/http'
require 'spreadsheet'
require 'json'

require 'open-uri'
require 'nokogiri'


Spreadsheet.client_encoding = 'UTF-8'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DROP TABLE swdata'
end

BASE_URL = 'http://www.halifax.ca/councillors/index.html'
doc = Nokogiri::HTML(open(BASE_URL))
url = doc.at_xpath('//*[@id="content_main"]/p[7]/a')['href']

Net::HTTP.start('www.halifax.ca') do |http|
  resp = http.get(url)
  open("councillors.xls","wb") do |file|
    file.write(resp.body)
  end
  book = Spreadsheet.open("councillors.xls") 
  book.worksheet(0).drop(1).each do |row|
    next if row[0].nil? 
    councillor = {
      name: row[1],
      district_name: row[0].split('-').drop(1).join('-'),
      elected_office: 'Councillor',
      source_url: BASE_URL,
      email: row[7],
      district_id: row[0].split('-').first,
      offices: [
        postal: row[2]+', '+row[3]+', '+row[4]+', '+row[5],
        tel: row[6],
      ] 
    }
    councillor[:offices] = councillor[:offices].to_json
    ScraperWiki.save_sqlite(['district_name'], councillor)
  end
end