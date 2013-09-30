require 'scraperwiki'
require 'nokogiri'           

urls = [
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ak-to-az-and-co-to-ky.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-la-to-nc.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-nd-to-ny.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-oh-to-or.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-pa-to-wy.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-wa.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-alameda-to-monterey.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-napa.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-nevada-to-sanmateo.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-santa-barbara-to-yuba.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-sonoma.htm'
 ]

wineries = []
urls.each do |url|
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  count = -1
  for row in doc.search('table')[1].search("tr")
    count += 1
    next if count == 0

    cells = row.search('td')
    data = {
      'permit_number' => cells[0].inner_text,
      'owner_name' => cells[1].inner_text,
      'operating_name' => cells[2].inner_text,
      'street' => cells[3].inner_text,
      'city' => cells[4].inner_text,
      'state' => cells[5].inner_text,
      'zip' => cells[6].inner_text,
      'zip4' => cells[7].inner_text,
      'county' => cells[8].inner_text
    }
    wineries << data 
    if data['owner_name'] && data['owner_name'] != ''
      wineries << data
      ScraperWiki.save_sqlite(unique_keys=['permit_number'], data=data)
    end
  end
end

puts wineries.to_jsonrequire 'scraperwiki'
require 'nokogiri'           

urls = [
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ak-to-az-and-co-to-ky.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-la-to-nc.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-nd-to-ny.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-oh-to-or.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-pa-to-wy.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-wa.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-alameda-to-monterey.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-napa.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-nevada-to-sanmateo.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-santa-barbara-to-yuba.htm',
  'http://www.ttb.treas.gov/foia/xls/frl-wine-producers-and-blenders-ca-sonoma.htm'
 ]

wineries = []
urls.each do |url|
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  count = -1
  for row in doc.search('table')[1].search("tr")
    count += 1
    next if count == 0

    cells = row.search('td')
    data = {
      'permit_number' => cells[0].inner_text,
      'owner_name' => cells[1].inner_text,
      'operating_name' => cells[2].inner_text,
      'street' => cells[3].inner_text,
      'city' => cells[4].inner_text,
      'state' => cells[5].inner_text,
      'zip' => cells[6].inner_text,
      'zip4' => cells[7].inner_text,
      'county' => cells[8].inner_text
    }
    wineries << data 
    if data['owner_name'] && data['owner_name'] != ''
      wineries << data
      ScraperWiki.save_sqlite(unique_keys=['permit_number'], data=data)
    end
  end
end

puts wineries.to_json