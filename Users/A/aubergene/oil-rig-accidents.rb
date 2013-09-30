###############################################################################
# Testing Nokogiri
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://home.versatel.nl/the_sims/rig/losses.htm'
doc = Nokogiri.HTML(ScraperWiki.scrape(starting_url))

table = doc.css("table")[1]

headers = table.css("th").map(&:text)
puts headers.inspect

# use Hpricot to get all <td> tags
table.css('tr')[1..-1].each do |tr|
    record = {}
    tr.css("td").each_with_index do |td, index|
      record[headers[index]] = td.text
    end
    puts record.inspect
    ScraperWiki.save(headers[0,2], record)
end
###############################################################################
# Testing Nokogiri
###############################################################################

require 'nokogiri'

# retrieve a page
starting_url = 'http://home.versatel.nl/the_sims/rig/losses.htm'
doc = Nokogiri.HTML(ScraperWiki.scrape(starting_url))

table = doc.css("table")[1]

headers = table.css("th").map(&:text)
puts headers.inspect

# use Hpricot to get all <td> tags
table.css('tr')[1..-1].each do |tr|
    record = {}
    tr.css("td").each_with_index do |td, index|
      record[headers[index]] = td.text
    end
    puts record.inspect
    ScraperWiki.save(headers[0,2], record)
end
