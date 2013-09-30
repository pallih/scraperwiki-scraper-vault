require 'httpclient'

ScraperWiki::attach("museum_top_level_domains")           
museums = ScraperWiki::select("* from museum_top_level_domains.swdata limit 5")

clnt = HTTPClient.new
threads = []

museums.each do |museum|
  url = museum["url"]
  name = museum["name"]

  threads << Thread.new(url) do |request|
    begin
      response = clnt.head(request)
      data = {
        url: url,
        name: name,
        status: response.status,
        redirect: response.headers["Location"] 
      }    
      ScraperWiki::save_sqlite(['url'], data) 
    rescue Exception => e
      data = {
        url: url,
        name: name,
        status: e.message
      }        
      ScraperWiki::save_sqlite(['url'], data) 
    end
  end

end

threads.each do |thread|
  thread.join
end
require 'httpclient'

ScraperWiki::attach("museum_top_level_domains")           
museums = ScraperWiki::select("* from museum_top_level_domains.swdata limit 5")

clnt = HTTPClient.new
threads = []

museums.each do |museum|
  url = museum["url"]
  name = museum["name"]

  threads << Thread.new(url) do |request|
    begin
      response = clnt.head(request)
      data = {
        url: url,
        name: name,
        status: response.status,
        redirect: response.headers["Location"] 
      }    
      ScraperWiki::save_sqlite(['url'], data) 
    rescue Exception => e
      data = {
        url: url,
        name: name,
        status: e.message
      }        
      ScraperWiki::save_sqlite(['url'], data) 
    end
  end

end

threads.each do |thread|
  thread.join
end
