# coding: utf-8

require 'json'
require 'open-uri'

require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

SOURCE_URL = 'http://www.kitchener.ca/en/insidecityhall/WhoIsMyCouncillor.asp'

doc = Nokogiri::HTML(open(SOURCE_URL))

doc.css('#printArea li').each do |li|
  name = li.at_css('strong').text.sub(/[ -]+\z/, '')
  a = li.at_css('a')

  url = if a[:href][/^http/]
    a[:href].sub('https', 'http')
  else
    "http://www.kitchener.ca#{a[:href]}"
  end

  doc = Nokogiri::HTML(open(url))
  para = doc.xpath('//p[contains(.,"Coun.")]')
  text = para.text
  personal_url = text[/Website: (\S+)/, 1]
  personal_url = "http://#{personal_url}" if personal_url && !personal_url[/\Ahttp/]

  email = text[/Email: (\S+)/, 1]
  unless email
    email = para.at_xpath('//a[starts-with(@href,"mailto:")]')[:href].sub('mailto:', '')
  end
  email = email.gsub(/[[:space:]]+/, ' ').strip

  photo_url = doc.at_css('#sideBar img')[:src]
  photo_url = "http://www.kitchener.ca#{photo_url}" if photo_url[%r{\A/}]

  data = {
    name: a.text.sub('Councillor ', '').gsub(/[[:space:]]+/, ' ').strip,
    elected_office: 'Councillor',
    email: email,
    district_id: name[/\d+/],
    district_name: name,
    url: url,
    photo_url: photo_url,
    personal_url: personal_url,
    source_url: SOURCE_URL,
  }

  tel = text[/City hall: (\S+)/, 1]
  fax = text[/Fax: (\S+)/, 1]
  if tel || fax
    office = {}
    office[:tel] = tel
    office[:fax] = fax
    data[:offices] = [office].to_json
  end

  ScraperWiki.save_sqlite(['district_id'], data)
end

source_url = 'http://www.kitchener.ca//en/insidecityhall/MayorSLandingPage.asp'

doc = Nokogiri::HTML(open(source_url))

photo_url = doc.at_css('#sideBar img')[:src]
photo_url = "http://www.kitchener.ca#{photo_url}" if photo_url[%r{\A/}]

data = {
  name: doc.at_css('h1').text.sub('Mayor ', '').gsub(/[[:space:]]+/, ' ').strip,
  elected_office: 'Mayor',
  district_id: 0,
  url: source_url,
  photo_url: photo_url,
  boundary_url: '/boundaries/census-subdivisions/3530013/',
  source_url: source_url,
}

email = doc.at_xpath('//a[starts-with(@href,"mailto:")]')
data[:email] = email[:href].sub('mailto:', '') if email

ScraperWiki.save_sqlite(['district_id'], data)
# coding: utf-8

require 'json'
require 'open-uri'

require 'nokogiri'

unless ScraperWiki.select('name FROM sqlite_master WHERE type="table" AND name="swdata"').empty? 
  ScraperWiki.sqliteexecute 'DELETE FROM swdata'
end

SOURCE_URL = 'http://www.kitchener.ca/en/insidecityhall/WhoIsMyCouncillor.asp'

doc = Nokogiri::HTML(open(SOURCE_URL))

doc.css('#printArea li').each do |li|
  name = li.at_css('strong').text.sub(/[ -]+\z/, '')
  a = li.at_css('a')

  url = if a[:href][/^http/]
    a[:href].sub('https', 'http')
  else
    "http://www.kitchener.ca#{a[:href]}"
  end

  doc = Nokogiri::HTML(open(url))
  para = doc.xpath('//p[contains(.,"Coun.")]')
  text = para.text
  personal_url = text[/Website: (\S+)/, 1]
  personal_url = "http://#{personal_url}" if personal_url && !personal_url[/\Ahttp/]

  email = text[/Email: (\S+)/, 1]
  unless email
    email = para.at_xpath('//a[starts-with(@href,"mailto:")]')[:href].sub('mailto:', '')
  end
  email = email.gsub(/[[:space:]]+/, ' ').strip

  photo_url = doc.at_css('#sideBar img')[:src]
  photo_url = "http://www.kitchener.ca#{photo_url}" if photo_url[%r{\A/}]

  data = {
    name: a.text.sub('Councillor ', '').gsub(/[[:space:]]+/, ' ').strip,
    elected_office: 'Councillor',
    email: email,
    district_id: name[/\d+/],
    district_name: name,
    url: url,
    photo_url: photo_url,
    personal_url: personal_url,
    source_url: SOURCE_URL,
  }

  tel = text[/City hall: (\S+)/, 1]
  fax = text[/Fax: (\S+)/, 1]
  if tel || fax
    office = {}
    office[:tel] = tel
    office[:fax] = fax
    data[:offices] = [office].to_json
  end

  ScraperWiki.save_sqlite(['district_id'], data)
end

source_url = 'http://www.kitchener.ca//en/insidecityhall/MayorSLandingPage.asp'

doc = Nokogiri::HTML(open(source_url))

photo_url = doc.at_css('#sideBar img')[:src]
photo_url = "http://www.kitchener.ca#{photo_url}" if photo_url[%r{\A/}]

data = {
  name: doc.at_css('h1').text.sub('Mayor ', '').gsub(/[[:space:]]+/, ' ').strip,
  elected_office: 'Mayor',
  district_id: 0,
  url: source_url,
  photo_url: photo_url,
  boundary_url: '/boundaries/census-subdivisions/3530013/',
  source_url: source_url,
}

email = doc.at_xpath('//a[starts-with(@href,"mailto:")]')
data[:email] = email[:href].sub('mailto:', '') if email

ScraperWiki.save_sqlite(['district_id'], data)
