require 'csv'
require 'open-uri'
OpenSSL::SSL::VERIFY_PEER = OpenSSL::SSL::VERIFY_NONE

# Unzipped data from http://auspost.com.au/products-and-services/download-postcode-data.html
# is in this gist https://gist.github.com/1504216 so we can just read it in

CSV.foreach(open('https://raw.github.com/gist/1504216/2b32590d354baf4a34e7a684c129186cf944e4e8/pc-full_20111123.csv'), headers: true) do |r|
  record = r.to_hash
  ScraperWiki.save_sqlite ['Pcode', 'Locality'], record
end

