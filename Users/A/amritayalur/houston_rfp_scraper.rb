# Blank Ruby

# Blank Ruby

html = ScraperWiki::scrape("http://purchasing.houstontx.gov/bid_download.aspx")

require 'nokogiri'
doc = Nokogiri::HTML html

doc.xpath('//text()').each do |node|
  if node.content=~/\S/
    node.content = node.content.strip
  else
    node.remove
  end
end



#document = doc.search("table#rptBidTypes__ctl0_dgResults > tr")



 doc.each do |v|
   cells = v.search 'td'
   #if cells.inner_html.length > 0
   link = v.search 'a'
   data = {
   number: puts (v.search("table#rptBidTypes__ctl0_dgResults > tr > td[1]").map(&:text))
      
   }
    #end
    ScraperWiki::save_sqlite(['number'], data)
 end



# Blank Ruby

# Blank Ruby

html = ScraperWiki::scrape("http://purchasing.houstontx.gov/bid_download.aspx")

require 'nokogiri'
doc = Nokogiri::HTML html

doc.xpath('//text()').each do |node|
  if node.content=~/\S/
    node.content = node.content.strip
  else
    node.remove
  end
end



#document = doc.search("table#rptBidTypes__ctl0_dgResults > tr")



 doc.each do |v|
   cells = v.search 'td'
   #if cells.inner_html.length > 0
   link = v.search 'a'
   data = {
   number: puts (v.search("table#rptBidTypes__ctl0_dgResults > tr > td[1]").map(&:text))
      
   }
    #end
    ScraperWiki::save_sqlite(['number'], data)
 end



