require 'nokogiri'
require 'net/http'
require 'uri'

def fetch(uri, original_uri, limit=10)
  if limit < 1
    warn "falling down a rabbit hole, no longer trying to reach #{original_uri}"
    return nil
  else
    begin
      response = Net::HTTP.get_response(URI.parse(uri))
    rescue Exception => fail
      if fail.message =~ /\: Name or service not known/
        #socket error, worth retrying
        fetch(uri, original_uri, limit-1)
      else
        warn "unexpected error reaching #{uri} - #{fail.message} [ original url: #{original_uri} ]"     
        return nil
      end
    rescue Timeout::Error
      sleep(20)
      fetch(original_uri, original_uri, limit-1)
    end
    case response.code
      when "200"
        return response.body
      when "404"
        warn "Couldn't find page #{uri}, skipping"
        return nil
      when "403"
        warn "Couldn't contact page #{uri} - may not be scraper-friendly, skipping"
        return nil
      when "301", "302"
        #redirected, follow
        fetch(response['location'], original_uri, limit-1)
      else
        warn "got a #{response.code} response, wasn't expecting that - url: #{uri}"
        return nil
    end
  end
end

# retrieve a page
starting_url = 'http://www.collectandgo.be/cogo/nl/home'
response = fetch(starting_url, starting_url)
p responserequire 'nokogiri'
require 'net/http'
require 'uri'

def fetch(uri, original_uri, limit=10)
  if limit < 1
    warn "falling down a rabbit hole, no longer trying to reach #{original_uri}"
    return nil
  else
    begin
      response = Net::HTTP.get_response(URI.parse(uri))
    rescue Exception => fail
      if fail.message =~ /\: Name or service not known/
        #socket error, worth retrying
        fetch(uri, original_uri, limit-1)
      else
        warn "unexpected error reaching #{uri} - #{fail.message} [ original url: #{original_uri} ]"     
        return nil
      end
    rescue Timeout::Error
      sleep(20)
      fetch(original_uri, original_uri, limit-1)
    end
    case response.code
      when "200"
        return response.body
      when "404"
        warn "Couldn't find page #{uri}, skipping"
        return nil
      when "403"
        warn "Couldn't contact page #{uri} - may not be scraper-friendly, skipping"
        return nil
      when "301", "302"
        #redirected, follow
        fetch(response['location'], original_uri, limit-1)
      else
        warn "got a #{response.code} response, wasn't expecting that - url: #{uri}"
        return nil
    end
  end
end

# retrieve a page
starting_url = 'http://www.collectandgo.be/cogo/nl/home'
response = fetch(starting_url, starting_url)
p response