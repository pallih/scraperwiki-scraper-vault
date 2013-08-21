require 'nokogiri'

URL = "http://www.opinionsuite.com/sutton"

doc = Nokogiri.HTML(ScraperWiki.scrape(URL))

doc.search("li#widget-open tbody tr").each do |consultation|
  data = {}
  data[:title] = consultation.search("td")[0].at("a").inner_text.strip
  data[:link] = consultation.search("td")[0].at("a")[:href]
  data[:end_date] = Date.parse(consultation.search("td")[1].inner_text.strip)
  ScraperWiki::save_sqlite([:link], data)
end
