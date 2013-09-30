# Blank Ruby
require 'cgi'
require 'json'

sourcescraper = 'the_business_registry_of_norway'
ScraperWiki::attach(sourcescraper)

params = CGI::parse( ENV['QUERY_STRING'] )

if params.has_key? "orgnr"

  data = ScraperWiki::select(           
    "* from #{sourcescraper}.swdata where orgnr="+params["orgnr"].first
  )

  puts data.to_json
else
  puts "No data without an orgnr: https://views.scraperwiki.com/run/norwegian_business/?orgnr=%9d"
end# Blank Ruby
require 'cgi'
require 'json'

sourcescraper = 'the_business_registry_of_norway'
ScraperWiki::attach(sourcescraper)

params = CGI::parse( ENV['QUERY_STRING'] )

if params.has_key? "orgnr"

  data = ScraperWiki::select(           
    "* from #{sourcescraper}.swdata where orgnr="+params["orgnr"].first
  )

  puts data.to_json
else
  puts "No data without an orgnr: https://views.scraperwiki.com/run/norwegian_business/?orgnr=%9d"
end