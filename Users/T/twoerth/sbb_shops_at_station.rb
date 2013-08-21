require 'json'
require 'open-uri'
require 'nokogiri'

stations = JSON.parse( open( 'http://api.scraperwiki.com/api/1.0/datastore/sqlite?format=jsondict&name=sbb_premium_stations&query=select%20*%20from%20%60swdata%60%20limit%20100').read )


stations.each do |station|
  puts station['href']
  station_doc = Nokogiri::HTML( open( "http://www.sbb.ch#{ station['href'] }" ) )

  begin
    shop = station_doc.search('.parbase li h2 a')[0]
    shop_list_url = shop.attribute('href').to_s
  rescue
    puts "did not work out"
    next
  end

  begin
    shops_doc = Nokogiri::HTML( open( "http://www.sbb.ch#{ shop_list_url }" ) )
  rescue
    puts "couldn't open shops link"
    next
  end

  shops_doc.search('.shoplist ul.base li a').each do |link|
    begin
      data = {
        'station' => station['title'],
        'href' => link.attribute('href').to_s,
        'title' => link.content
      }

      ScraperWiki.save_sqlite(unique_keys=["href"], data)
    rescue
      puts 'failed...'
    end
  end
end