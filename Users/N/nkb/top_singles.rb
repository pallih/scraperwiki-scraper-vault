require 'nokogiri'

html = ScraperWiki.scrape("http://www.chartsinfrance.net/charts/8444/singles.php")           

doc = Nokogiri::HTML(html)
doc.xpath('/html').each do |node|
  puts html
end

