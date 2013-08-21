require 'cgi'  

paramdict = CGI::parse( ENV['QUERY_STRING'] )
p paramdict

ScraperWiki::attach("tutorialscraper_5") 

data = ScraperWiki::select(           
    "* from tutorialscraper_5.swdata 
    order by years_in_school desc limit 10"
)
#puts data

         
