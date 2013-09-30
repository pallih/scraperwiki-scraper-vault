
html = ScraperWiki::scrape("http://mission.sfgov.org/OCABidPublication/ReviewBids.aspx")



require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr").each do |v|
  cells = v.search 'td'
  if cells.count == 6
    data = {
      bid: v[1].inner_html,
      due_date: v[2].inner_html,
      
    }
    ScraperWiki::save_sqlite(['bid'], data)
  end
end

html = ScraperWiki::scrape("http://mission.sfgov.org/OCABidPublication/ReviewBids.aspx")



require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr").each do |v|
  cells = v.search 'td'
  if cells.count == 6
    data = {
      bid: v[1].inner_html,
      due_date: v[2].inner_html,
      
    }
    ScraperWiki::save_sqlite(['bid'], data)
  end
end
