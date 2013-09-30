puts "Scraping recent posts from the PETA blog!"

html = ScraperWiki.scrape("http://www.peta.org/b/thepetafiles/default.aspx")

require 'nokogiri'           

doc = Nokogiri::HTML(html)

for v in doc.xpath("//div[@class = 'abbreviated-post']//h1[@class = 'post-name']//a[@class = 'internal-link view-post']")

  data = {
    'title' => v.text,
    'url' => v['href'],
  }

  #puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['url'], data=data)
end


puts "Scraping recent posts from the PETA blog!"

html = ScraperWiki.scrape("http://www.peta.org/b/thepetafiles/default.aspx")

require 'nokogiri'           

doc = Nokogiri::HTML(html)

for v in doc.xpath("//div[@class = 'abbreviated-post']//h1[@class = 'post-name']//a[@class = 'internal-link view-post']")

  data = {
    'title' => v.text,
    'url' => v['href'],
  }

  #puts data.to_json
  ScraperWiki.save_sqlite(unique_keys=['url'], data=data)
end


