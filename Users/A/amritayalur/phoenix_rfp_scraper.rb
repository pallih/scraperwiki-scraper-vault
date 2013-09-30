# Blank Ruby

html = ScraperWiki::scrape("http://phoenix.gov/business/contract/opportunities/solicitations/index.html")

require 'nokogiri'
doc = Nokogiri::HTML html

doc.xpath('//text()').each do |node|
  if node.content=~/\S/
    node.content = node.content.strip
  else
    node.remove
  end
end



 doc.search("table tr").each do |v|
  cells = v.search 'td'
  if cells.inner_html.length > 0
    link = v.search 'a'
    data = {
      bid: cells.children.text,
      link: "http://phoenix.gov" + link.attr('href').text,
    }
   end
   ScraperWiki::save_sqlite(['bid'], data)
 end


# Blank Ruby

html = ScraperWiki::scrape("http://phoenix.gov/business/contract/opportunities/solicitations/index.html")

require 'nokogiri'
doc = Nokogiri::HTML html

doc.xpath('//text()').each do |node|
  if node.content=~/\S/
    node.content = node.content.strip
  else
    node.remove
  end
end



 doc.search("table tr").each do |v|
  cells = v.search 'td'
  if cells.inner_html.length > 0
    link = v.search 'a'
    data = {
      bid: cells.children.text,
      link: "http://phoenix.gov" + link.attr('href').text,
    }
   end
   ScraperWiki::save_sqlite(['bid'], data)
 end


