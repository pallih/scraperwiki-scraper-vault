html = ScraperWiki::scrape("http://judis.nic.in/supremecourt/Chrseq.aspx")
p html

require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr.tcont").each do |v|
  cells = v.search 'td'
  data = {
    country: cells[0].inner_html,
    years_in_school: cells[4].inner_html.to_i
  }
  ScraperWiki::save_sqlite(['country'], data)
end


