url = "http://hackerspaces.org/wiki/Special:Ask/-5B-5BCategory:Person-5D-5D/mainlabel=Person/-3FCountry/-3FCity/-3Fhomepage/-3Femail/?limit=500&format=csv"
data = ScraperWiki.scrape(url)
ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
data = ic.iconv(data + ' ')[0..-2]
require 'csv'
csv = CSV.new(data, :headers => true)
for row in csv
  ScraperWiki.save_sqlite(unique_keys=['Person'], row.to_hash)
end
url = "http://hackerspaces.org/wiki/Special:Ask/-5B-5BCategory:Person-5D-5D/mainlabel=Person/-3FCountry/-3FCity/-3Fhomepage/-3Femail/?limit=500&format=csv"
data = ScraperWiki.scrape(url)
ic = Iconv.new('UTF-8//IGNORE', 'UTF-8')
data = ic.iconv(data + ' ')[0..-2]
require 'csv'
csv = CSV.new(data, :headers => true)
for row in csv
  ScraperWiki.save_sqlite(unique_keys=['Person'], row.to_hash)
end
