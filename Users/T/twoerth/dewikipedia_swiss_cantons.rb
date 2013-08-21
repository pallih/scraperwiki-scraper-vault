require 'nokogiri'           
require 'open-uri'

doc = Nokogiri::HTML( open( "http://de.wikipedia.org/wiki/Kanton_(Schweiz)" ) )

cantons = {}

doc.xpath('//div[@id="mw-content-text"]/table[3]/tr').each do |tr|
  tds = tr.css('td')
  
  next unless tds.size == 6

  cantons[ tds[1].content.to_i ] = {
    '_id' => 'K_' + tds[1].content.to_i.to_s,
    'iso' => tds[0].content,
    'link' => tds[2].css('a').attribute('href').to_s.gsub('/wiki/',''),
    'name' => {
      'de' => tds[2].content,
      'fr' => tds[3].content,
      'it' => tds[4].content,
      'rm' => tds[5].content,
    }
  }

end

index = 1

doc.xpath('//div[@id="mw-content-text"]/table[2]/tr').each do |tr|
  tds = tr.css('td')
  puts tds.size

  next unless tds.size == 12 && index < 27

  cantons[ index ][ 'wappen' ] = tds[0].css('a img').attribute('src').to_s
  cantons[ index ][ 'link' ] = tds[1].css('a').attribute('href').to_s.gsub('/wiki/','')
  
  index += 1
end

puts cantons.inspect