require 'zlib'

tags = ["android", "c", "git", "go", "google-app-engine", "linux", "ruby", "sqlite", "vim", "xml"]
data = Hash.new()
data["timestamp"] = Time.now.getutc

tags.each do |x|
  uri = ScraperWiki::scrape("https://api.stackexchange.com/2.1/tags/" + x + "/info?site=stackoverflow")
  gz = Zlib::GzipReader.new(StringIO.new(uri))
  doc = gz.read
  data[x] = doc[/count.:[0-9]+/][/[0-9]+/]
end

ScraperWiki::save_sqlite(
  unique_keys = ["timestamp"],
  data
)require 'zlib'

tags = ["android", "c", "git", "go", "google-app-engine", "linux", "ruby", "sqlite", "vim", "xml"]
data = Hash.new()
data["timestamp"] = Time.now.getutc

tags.each do |x|
  uri = ScraperWiki::scrape("https://api.stackexchange.com/2.1/tags/" + x + "/info?site=stackoverflow")
  gz = Zlib::GzipReader.new(StringIO.new(uri))
  doc = gz.read
  data[x] = doc[/count.:[0-9]+/][/[0-9]+/]
end

ScraperWiki::save_sqlite(
  unique_keys = ["timestamp"],
  data
)