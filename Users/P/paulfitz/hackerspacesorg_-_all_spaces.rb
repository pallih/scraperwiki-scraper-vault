# D'oh. This turns out to be very easy, the wiki will serve csv...

offset = 0
while true do
  url = "http://hackerspaces.org/wiki/Special:Ask/-5B-5BCategory:Hackerspace-5D-5D/-3FCountry/-3FState/-3FCity/-3FWebsite/-3FDate-20of-20founding/-3FHackerspace-20status/mainlabel%3DHackerspace/order%3DASC/sort%3DCountry?format=csv&limit=10000"
  data = ScraperWiki.scrape(url + "&offset=#{offset}")
  ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
  data = ic.iconv(data + ' ')[0..-2]
  require 'csv'
  csv = CSV.new(data, :headers => true)
  ct = 0
  for row in csv
    ct = ct+1
    # print "working on #{row.inspect}\n"
    ScraperWiki.save_sqlite(unique_keys=['Hackerspace'], row.to_hash)
  end
  # print "Read #{ct} rows\n"
  break unless ct>0
  offset = offset + ct
end

# Hack to update view
ScraperWiki.commit
ScraperWiki.scrape("https://views.scraperwiki.com/run/hackerspace_changes/?")
