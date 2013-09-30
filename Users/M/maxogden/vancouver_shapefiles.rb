require 'nokogiri'

doc = Nokogiri::HTML.parse(ScraperWiki.scrape('http://data.vancouver.ca/datacatalogue/index.htm'))

doc.css("a").each do |link|
  if link.attr('href') =~ /shape/
    ScraperWiki.save(['href'], {'href' => link.attr('href')})
  end
endrequire 'nokogiri'

doc = Nokogiri::HTML.parse(ScraperWiki.scrape('http://data.vancouver.ca/datacatalogue/index.htm'))

doc.css("a").each do |link|
  if link.attr('href') =~ /shape/
    ScraperWiki.save(['href'], {'href' => link.attr('href')})
  end
end