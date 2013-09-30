require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.gardencentreguide.co.uk'

def extract(page,css)
  element = page.at_css(css)
  if element
    element.inner_text
  else
    nil
  end
end

main_page = Nokogiri::HTML(open(BASE_URL))
main_page.css('div.SEO_links li a').collect do |county|
  county_name = county['href'].split('/')[-1].capitalize
  begin
    county_page = Nokogiri::HTML(open(county['href']))
  rescue Exception => e
    next if e.message =~ /404/
    raise e
  end
  county_page.css('ul#cities li a').collect do |nursery|
    primary_key = nursery['href']
    puts "  #{primary_key}"
    gc = Nokogiri::HTML(open(BASE_URL+primary_key))
    record = {}
    record['primary_key'] = primary_key
    record['name']        = extract(gc,'h1.groen span')
    record['address']     = extract(gc,'td.street-address')
    record['town']        = extract(gc,'td.locality')
    record['postal_code'] = extract(gc,'td.postal-code')
    record['phone']       = extract(gc,'td.tel span.value')
    record['county']      = county_name
    ScraperWiki.save(['primary_key'], record)
  end
end

require 'nokogiri'
require 'open-uri'

BASE_URL = 'http://www.gardencentreguide.co.uk'

def extract(page,css)
  element = page.at_css(css)
  if element
    element.inner_text
  else
    nil
  end
end

main_page = Nokogiri::HTML(open(BASE_URL))
main_page.css('div.SEO_links li a').collect do |county|
  county_name = county['href'].split('/')[-1].capitalize
  begin
    county_page = Nokogiri::HTML(open(county['href']))
  rescue Exception => e
    next if e.message =~ /404/
    raise e
  end
  county_page.css('ul#cities li a').collect do |nursery|
    primary_key = nursery['href']
    puts "  #{primary_key}"
    gc = Nokogiri::HTML(open(BASE_URL+primary_key))
    record = {}
    record['primary_key'] = primary_key
    record['name']        = extract(gc,'h1.groen span')
    record['address']     = extract(gc,'td.street-address')
    record['town']        = extract(gc,'td.locality')
    record['postal_code'] = extract(gc,'td.postal-code')
    record['phone']       = extract(gc,'td.tel span.value')
    record['county']      = county_name
    ScraperWiki.save(['primary_key'], record)
  end
end

