# Blank Ruby

require 'json'
require 'open-uri'

baseurl = "http://hotell.difi.no/api/json/brreg/enhetsregisteret"

def save_entries(url)
  page = open url
  data = JSON.parse page.readlines.first
  @count = data["pages"] if data["page"] == 1
  data["entries"].each do |entry|
    ScraperWiki::save_sqlite(unique_keys=entry.keys, entry)
  end
end

# Save the first entry to set @count
save_entries baseurl

i=2
while i <= @count do
  save_entries baseurl + "?page=#{i}"
  i += 1
end