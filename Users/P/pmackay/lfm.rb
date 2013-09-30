# Blank Ruby
require 'nokogiri'

html = ScraperWiki::scrape "http://www.lfm.org.uk/markets-home/"
# p html

doc = Nokogiri::HTML html
doc.search("table[@class='summary-list'] tr").each do |v|
  # cells = v.search 'td'
  name = v.xpath('td//a')
  if name.length > 0
    p name[1].content.strip
  end
#  p cells[1].xpath('/a')[0].content
end

