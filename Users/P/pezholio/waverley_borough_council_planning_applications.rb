require 'rss'
require 'open-uri'

url = 'http://waverweb.waverley.gov.uk/rssfeeds.nsf/rss?openagent&uid=8425C79F9687E70D80257A8600556EDF'

open(url) do |rss|
  feed = RSS::Parser.parse(rss)

  feed.items.each do |item|
    details = {}

    details[:url] = item.link
    details[:date] = item.pubDate
    
    title = item.title.split(':')

    details[:address] = title[0].strip
    details[:proposal] = title[1].strip
    details[:postcode] = details[:address].match('([A-PR-UWYZ]([0-9]{1,2}|([A-HK-Y][0-9]|[A-HK-Y][0-9]([0-9]|[ABEHMNPRV-Y]))|[0-9][A-HJKPS-UW]) [0-9][ABD-HJLNP-UW-Z]{2})')[0]

    doc = JSON.parse open("http://www.uk-postcodes.com/postcode/#{details[:postcode].gsub(' ', '').upcase}.json").read

    details[:easting] = doc['geo']['easting']
    details[:northing] = doc['geo']['northing']
    details[:lat] = doc['geo']['lat']
    details[:lng] = doc['geo']['lng']

    ScraperWiki.save([:url], details)

  end
end

