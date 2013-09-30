# Monkeypatch!

def ScraperWiki._scrape_uri_with_redirect(uri, limit = 10)
  # You should choose better exception.
  raise ArgumentError, 'HTTP redirect too deep' if limit == 0

  response = Net::HTTP.get_response(uri)
  case response
  when Net::HTTPSuccess     then response
  when Net::HTTPRedirection then _scrape_uri_with_redirect(uri.merge(response['location']), limit - 1)
  else
    response.error!
  end
end

def ScraperWiki.scrape (url, params = nil)
  uri  = URI.parse(url)
  if params.nil? 
      data = ScraperWiki._scrape_uri_with_redirect(uri).body
  else
      if uri.path = ''
          uri.path = '/' # must post to a path
      end
      data = Net::HTTP.post_form(uri, params)
  end
  return data
end

print ScraperWiki.scrape('http://www.decc.gov.uk/Media/viewfile.ashx?FilePath=Consultations/plutonium-stocks/1243-uk-plutonium-stocks.pdf&filetype=4')

# Monkeypatch!

def ScraperWiki._scrape_uri_with_redirect(uri, limit = 10)
  # You should choose better exception.
  raise ArgumentError, 'HTTP redirect too deep' if limit == 0

  response = Net::HTTP.get_response(uri)
  case response
  when Net::HTTPSuccess     then response
  when Net::HTTPRedirection then _scrape_uri_with_redirect(uri.merge(response['location']), limit - 1)
  else
    response.error!
  end
end

def ScraperWiki.scrape (url, params = nil)
  uri  = URI.parse(url)
  if params.nil? 
      data = ScraperWiki._scrape_uri_with_redirect(uri).body
  else
      if uri.path = ''
          uri.path = '/' # must post to a path
      end
      data = Net::HTTP.post_form(uri, params)
  end
  return data
end

print ScraperWiki.scrape('http://www.decc.gov.uk/Media/viewfile.ashx?FilePath=Consultations/plutonium-stocks/1243-uk-plutonium-stocks.pdf&filetype=4')

