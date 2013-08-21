# Blank Ruby
require 'nokogiri'
require 'uri'

html = ScraperWiki.scrape('http://www.cityofboston.gov/snow/storm.asp')
data = []
doc = Nokogiri::HTML.parse(html).css("select[name='selNeighborhood']").css("option").each do |n|
  n = n.text.strip
  next if n == "Choose Neighborhood"
  nHtml = ScraperWiki.scrape("http://www.cityofboston.gov/snow/storm.asp?selNeighborhood=#{URI.escape(n)}")
  nDoc = Nokogiri::HTML.parse(nHtml).css('.mainLeadStory tr').each do |tr|
    next if tr.text == ""
    row = tr.text.strip.split("\n\t\t\n\t\t\n\t\t\t")
    next if row.size > 2
    next if row[0] == "Street Name" || row[0] == "Varies by Neighborhood"
    sn = row[0] || ""
    ss = row[1] || ""
    ScraperWiki.save(unique_keys=['street_name', 'street_stretch', 'neighborhood'], data={"street_name" => sn, "street_stretch" => ss, "neighborhood" => n})
  end
end


