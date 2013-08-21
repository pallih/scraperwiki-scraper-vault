sourcescraper = 'baby_names'

ScraperWiki.attach("baby_names")
data = ScraperWiki.select("* from baby_names.swdata order by year,rank desc limit 10")
puts data
