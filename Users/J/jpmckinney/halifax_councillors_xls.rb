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
url = doc.at_xpath('//a[contains(@href,".xls")]')['href']

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
        tel: '902-'+row[6],
      ] 
    }
    councillor[:offices] = councillor[:offices].to_json
    ScraperWiki.save_sqlite(['district_name'], councillor)
  end
end


#### Mayor not included in xls, scraped separately here ####

MAYOR_URL = 'http://www.halifax.ca/mayor'
CONTACT_URL = MAYOR_URL+'/contact.php'

doc = Nokogiri::HTML(open(MAYOR_URL))
name = doc.at_xpath('//h1[contains(text(),"Bio")]').text.gsub('Bio','')

doc = Nokogiri::HTML(open(CONTACT_URL))
contact = doc.at_xpath('//*[@id="content_area"]//section[2]/p[2]')
mayor = {
  name: name.strip,
  district_name: '',
  elected_office: 'Mayor',
  source_url: MAYOR_URL,
  email: contact.at_xpath('./a').text,
  url: CONTACT_URL,
  district_id: '',
  boundary_url: '/boundaries/census-subdivisions/1209034/',
  offices: [
    postal: contact.text.match(/(Mailing Address:).+/).to_s.gsub('Mailing Address:','').strip,
    tel: contact.text.match(/[(0-9)]{5}.([0-9]{3}.){2}/).to_s
  ]
  
}
mayor[:offices] = mayor[:offices].to_json
ScraperWiki.save_sqlite(['district_name'], mayor)
  
