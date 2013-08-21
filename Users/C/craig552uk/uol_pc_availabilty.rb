# Scrape data about PC availability on University of Leicester Campus
# craig@craig-russell.co.uk

require 'hpricot'

def parse_qs(url)
  params = {}
  url.split('?')[1].split('&').each do |param|
    k = param.split('=')[0]
    v = param.split('=')[1]
    params[k.to_sym] = v
  end
  return params
end

url  = "http://opendata.le.ac.uk/mobappandroid/default.aspx"
doc  = Hpricot(ScraperWiki::scrape(url))
rows = doc.search('.repeaterStyle a')

rows.each do |row|
  lab = {}
  lab[:lat]     = parse_qs(row[:href])[:lat]
  lab[:lng]     = parse_qs(row[:href])[:lng]
  lab[:name]    = row.inner_html.split(' (')[0]
  lab[:num_pcs] = row.inner_html.split(' (')[1].gsub(')','')
  puts lab.inspect
  ScraperWiki::save_sqlite(unique_keys=[:name], data=lab)
end

