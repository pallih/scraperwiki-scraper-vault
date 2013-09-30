# Blank Ruby
html = ScraperWiki.scrape("http://directory.rakuten.co.jp/rms/sd/directory/vc/s3tz555091/")
puts html

require 'nokogiri'
doc = Nokogiri::HTML(html)
for v in doc.search("//td font")
  cells = v.search('a')
  data = {
    'shop' => cells[0].inner_html
  }
  puts data.to_json


  ScraperWiki.save_sqlite(unique_keys=['shop'], data=data)


end

# Blank Ruby
html = ScraperWiki.scrape("http://directory.rakuten.co.jp/rms/sd/directory/vc/s3tz555091/")
puts html

require 'nokogiri'
doc = Nokogiri::HTML(html)
for v in doc.search("//td font")
  cells = v.search('a')
  data = {
    'shop' => cells[0].inner_html
  }
  puts data.to_json


  ScraperWiki.save_sqlite(unique_keys=['shop'], data=data)


end

