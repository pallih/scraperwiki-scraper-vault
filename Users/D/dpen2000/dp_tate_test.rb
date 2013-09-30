# Blank Ruby
require 'scraperwiki'

ScraperWiki.attach('tate_liverpool_exhibitions_data', 'p')
foobar = ScraperWiki.select('lat, long, postcode_district from p.swdata where lat is not null group by postcode_district')
puts foobar
# Blank Ruby
require 'scraperwiki'

ScraperWiki.attach('tate_liverpool_exhibitions_data', 'p')
foobar = ScraperWiki.select('lat, long, postcode_district from p.swdata where lat is not null group by postcode_district')
puts foobar
