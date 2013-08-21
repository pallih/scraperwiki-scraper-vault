###############################################################################
# Basic scraper
###############################################################################

require 'hpricot'

# retrieve a page
starting_url = 'http://www.halstead.com/new.aspx'
html = ScraperWiki.scrape(starting_url)

doc = Hpricot(html)
doc.search('p').each do |para|
  p_text = para.inner_text
  next unless p_text =~ /^\d{3}/
  code, name = p_text.split(' ', 2)
  code = code.to_i
  puts [code, name].join(" - ")
  ScraperWiki.save(["Location","Price","Contact"], { "Location" => location, "Price" => price, "Contact" => contact } )
end


