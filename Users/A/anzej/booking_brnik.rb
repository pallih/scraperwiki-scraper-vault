# Blank Ruby

html = ScraperWiki.scrape("http://www.booking.com/searchresults.en.html?iata=LJU")

require 'nokogiri'           

doc = Nokogiri::HTML(html)

for v in doc.search("tr.flash_deal_soldout")

  hotel = {}
  hotel['Hotel ID'] = v.search('td').first().attr('id').gsub('hotel_', '')
  hotel['Hotel name'] = v.search('td h3 a').inner_html
  hotel['Hotel location'] = v.search('td.has-review div.address strong').inner_html
  hotel['www.booking.com'] = v.search('td h3 a').attr('href').to_s.gsub('/hotel/', 'www.booking.com/hotel/')
#.to_s translates this NODE (or something) into string
  hotel['latest booking'] = v.search('div.lbsr span.lastbooking').inner_text.gsub('Latest booking:', '').strip.gsub(/\n+/, "")  
# .strip removes all backspaces at the beginning and end of string , .gsub(/\n+/, "") removes all line break characters from string
  hotel['CET time'] = Time.new+(60*60*2)

  ScraperWiki.save(['Hotel ID'], hotel)
end

