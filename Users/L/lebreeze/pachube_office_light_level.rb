# Blank Ruby
require 'csv'
require 'fastercsv'

data = ScraperWiki.scrape("https://api.pachube.com/v2/feeds/504/datastreams/1.csv?key=ENLSV9ppvVnYR4O5miKh3s0sBoV41A3BpMIulOGGSA-9PZ12PCcQyGBcyXoRhgik88blsOsx7r_FS2lQJNq-WAbJZCQdnYm6lStAEj-BuwzOgXNd3U0DFfJf5bFo2w8R")

csv = CSV.new(data)
puts csv

for row in csv
  hash = {:timestamp => row[0], :value => row[1]}
  ScraperWiki.save_sqlite(unique_keys=['timestamp', 'value'], hash)
end
# Blank Ruby
require 'csv'
require 'fastercsv'

data = ScraperWiki.scrape("https://api.pachube.com/v2/feeds/504/datastreams/1.csv?key=ENLSV9ppvVnYR4O5miKh3s0sBoV41A3BpMIulOGGSA-9PZ12PCcQyGBcyXoRhgik88blsOsx7r_FS2lQJNq-WAbJZCQdnYm6lStAEj-BuwzOgXNd3U0DFfJf5bFo2w8R")

csv = CSV.new(data)
puts csv

for row in csv
  hash = {:timestamp => row[0], :value => row[1]}
  ScraperWiki.save_sqlite(unique_keys=['timestamp', 'value'], hash)
end
