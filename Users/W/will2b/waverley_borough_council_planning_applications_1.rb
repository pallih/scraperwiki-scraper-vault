require 'rss'
require 'open-uri'

url = 'https://www.mygov.je/Planning/Pages/Planning.aspx'

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

    doc = JSON.parse open("http://www.jerseypost.com/Personal/Sendingmail/Pages/Addressfinder.aspx#{details[:postcode].gsub(' ', '').upcase}.json").read

    details[:easting] = doc['geo']['easting']
    details[:northing] = doc['geo']['northing']

    ScraperWiki.save([:url], details)

  end
end