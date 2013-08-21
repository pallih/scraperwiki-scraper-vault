# coding: utf-8

require 'nokogiri'
require 'open-uri'
require 'yaml'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'

url = "http://www.jobs.bg/company/"
min_id = 0
max_id = 0
counter = 0
last_id = 'not found'

ids = ScraperWiki::select("MAX(ID) as MAX_ID FROM employers") rescue min_id = (2**(0.size * 8 -2) -1)

for v in ids
  min_id = v["MAX_ID"]
#  min_id = 180540
  max_id = min_id + 100
end

# for i in 25000..26000
for i in min_id..max_id
  doc = Nokogiri.HTML(open(url + i.to_s))
  doc.search('span[@style="font-size:29px;font-weight:bold;padding:20px;display:block;"]').each do |v|
#    p v.inner_text.strip
    data = {
      id: i,
      company_name: v.inner_text.strip,
      company_href: url + i.to_s
    }
    ScraperWiki::save_sqlite(unique_keys=['id'], data, table_name="employers", verbose=0)
    last_id = url + i.to_s
    counter = counter + 1
  end
end

p "for " + min_id.to_s + ".." + max_id.to_s + ": found - " + counter.to_s + " and the last is - " + last_id
