require 'hpricot'
require 'time'

url = "http://neo.jpl.nasa.gov/cgi-bin/neo_ca?type=NEO&hmax=all&sort=date&sdir=ASC&tlim=far_future&dmax=0.2AU&max_rows=0&action=Display+Table&show=1"
html = ScraperWiki.scrape(url)
doc = Hpricot(html)

table = doc.search("html > body > table > tr:nth(8) > td:nth(1) > center > table > tr:nth(1) > td > table > tr:nth(1) > td > table")
rows = table.search("//tr")
rows.shift

rows.each do |row|
  data = row.search("//td//font")

  if data.length == 8
    name = data[0].inner_html.gsub(/&nbsp;/, ' ').gsub(/\(|\)/, '').strip
    datetime = Time.parse(data[1].inner_html.gsub(/&nbsp;/, ' ').split('&plusmn;').first.strip + " UTC") # force UTC
    miss_norm_au = data[2].inner_html.split('/')[1].to_f
    miss_min_au = data[3].inner_html.split('/')[1].to_f
    v_relative = data[4].inner_html.to_s.to_f
    v_infinity = data[5].inner_html.to_s.to_f
    n_sigma = data[6].inner_html.to_f
    h = data[7].inner_html.to_f
    
    asteroid = {  'miss_norm_au' => miss_norm_au,
                  'miss_min_au' => miss_min_au,
                  'v_relative' => v_relative,
                  'v_infinity' => v_infinity,
                  'n_sigma' => n_sigma,
                  'h' => h, 
                  'name' => name }
                  
    ScraperWiki.save(['name'], asteroid, datetime, nil)
  end
end
require 'hpricot'
require 'time'

url = "http://neo.jpl.nasa.gov/cgi-bin/neo_ca?type=NEO&hmax=all&sort=date&sdir=ASC&tlim=far_future&dmax=0.2AU&max_rows=0&action=Display+Table&show=1"
html = ScraperWiki.scrape(url)
doc = Hpricot(html)

table = doc.search("html > body > table > tr:nth(8) > td:nth(1) > center > table > tr:nth(1) > td > table > tr:nth(1) > td > table")
rows = table.search("//tr")
rows.shift

rows.each do |row|
  data = row.search("//td//font")

  if data.length == 8
    name = data[0].inner_html.gsub(/&nbsp;/, ' ').gsub(/\(|\)/, '').strip
    datetime = Time.parse(data[1].inner_html.gsub(/&nbsp;/, ' ').split('&plusmn;').first.strip + " UTC") # force UTC
    miss_norm_au = data[2].inner_html.split('/')[1].to_f
    miss_min_au = data[3].inner_html.split('/')[1].to_f
    v_relative = data[4].inner_html.to_s.to_f
    v_infinity = data[5].inner_html.to_s.to_f
    n_sigma = data[6].inner_html.to_f
    h = data[7].inner_html.to_f
    
    asteroid = {  'miss_norm_au' => miss_norm_au,
                  'miss_min_au' => miss_min_au,
                  'v_relative' => v_relative,
                  'v_infinity' => v_infinity,
                  'n_sigma' => n_sigma,
                  'h' => h, 
                  'name' => name }
                  
    ScraperWiki.save(['name'], asteroid, datetime, nil)
  end
end
