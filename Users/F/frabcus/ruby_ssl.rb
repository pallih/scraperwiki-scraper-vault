require 'httpclient'

def ScraperWiki.scrape(url, params = nil)
  client = HTTPClient.new
  client.ssl_config.verify_mode = OpenSSL::SSL::VERIFY_NONE

  if params.nil? 
    return client.get_content(url)
  else
    return client.post_content(url, params)
  end
end

#starting_url = 'http://www.flourish.org'
starting_url = 'https://ppc.ipswich.gov.uk/appndetails.asp?iAppID=12/00618/FUL&sType=&search_params=pageNumber%3D1%26txtValStartDate%3D02%252F08%252F2012%26txtValEndDate%3D16%252F08%252F2012%26pnlAdvancedOpen%3D1pageNumber%253D1pageNumber%253D2pageNumber%253D3%26&prev_search_params=&det_search_params='
html = ScraperWiki.scrape(starting_url)
print html

print ScraperWiki.scrape("http://duckduckgo.com", { 'q'=>'cat' })
require 'httpclient'

def ScraperWiki.scrape(url, params = nil)
  client = HTTPClient.new
  client.ssl_config.verify_mode = OpenSSL::SSL::VERIFY_NONE

  if params.nil? 
    return client.get_content(url)
  else
    return client.post_content(url, params)
  end
end

#starting_url = 'http://www.flourish.org'
starting_url = 'https://ppc.ipswich.gov.uk/appndetails.asp?iAppID=12/00618/FUL&sType=&search_params=pageNumber%3D1%26txtValStartDate%3D02%252F08%252F2012%26txtValEndDate%3D16%252F08%252F2012%26pnlAdvancedOpen%3D1pageNumber%253D1pageNumber%253D2pageNumber%253D3%26&prev_search_params=&det_search_params='
html = ScraperWiki.scrape(starting_url)
print html

print ScraperWiki.scrape("http://duckduckgo.com", { 'q'=>'cat' })
