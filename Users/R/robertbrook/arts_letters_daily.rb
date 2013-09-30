require 'nokogiri'
require 'net/http'
require 'uri'

# now following redirects
# thanks to Ben G for the space-stripping tip

starting_url = 'http://www.aldaily.com/'
html = ScraperWiki.scrape(starting_url)


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

#adapted from http://snippets.dzone.com/posts/show/2384
def tidy_title(str)
  accents = { 
    ['á','à','â','ä','ã'] => 'a',
    ['Ã','Ä','Â','À','�?'] => 'A',
    ['é','è','ê','ë'] => 'e',
    ['Ë','É','È','Ê'] => 'E',
    ['í','ì','î','ï'] => 'i',
    ['�?','Î','Ì','�?'] => 'I',
    ['ó','ò','ô','ö','õ'] => 'o',
    ['Õ','Ö','Ô','Ò','Ó'] => 'O',
    ['ú','ù','û','ü'] => 'u',
    ['Ú','Û','Ù','Ü'] => 'U',
    ['ç'] => 'c', ['Ç'] => 'C',
    ['ñ'] => 'n', ['Ñ'] => 'N'
  }
  accents.each do |ac,rep|
    ac.each do |s|
      str = str.gsub(s, rep)
    end
  end
  str = str.gsub(/[^a-zA-Z0-9\.,;:\- \'\"\)\(\/\|\&\?\!]/,"")
  str = str.gsub(/[ ]+/," ")
  str = str.gsub(/&amp;/, "&")
  str = str.gsub(/&gt;/, ">")
  str.strip
end

doc = Nokogiri::HTML(html)
doc.search('a').each do |a|
  if a.inner_html =~ /more<b>/ then
    local_url = a['href'].strip
    if local_url
      #workaround for nymag.com's javascript generated print pages
      if local_url =~ /nymag.com\/print\/?\//
        local_url = local_url.gsub("/print/?/", "/")
      end
      local_html = fetch(local_url, a['href'])
      if local_html
        local_doc = Nokogiri::HTML(local_html)
        local_title = local_doc.search('title').inner_html
        #cheat due to lack of unicode gem (or lack of intelligence on my part - LC)
        local_title = tidy_title(local_title)
        begin
          record = {'link' => a['href'], 'title' => local_title}
          ScraperWiki.save(['link'], record)
        rescue
          raise local_title.inspect
        end
      end
    end
  end
end
require 'nokogiri'
require 'net/http'
require 'uri'

# now following redirects
# thanks to Ben G for the space-stripping tip

starting_url = 'http://www.aldaily.com/'
html = ScraperWiki.scrape(starting_url)


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

#adapted from http://snippets.dzone.com/posts/show/2384
def tidy_title(str)
  accents = { 
    ['á','à','â','ä','ã'] => 'a',
    ['Ã','Ä','Â','À','�?'] => 'A',
    ['é','è','ê','ë'] => 'e',
    ['Ë','É','È','Ê'] => 'E',
    ['í','ì','î','ï'] => 'i',
    ['�?','Î','Ì','�?'] => 'I',
    ['ó','ò','ô','ö','õ'] => 'o',
    ['Õ','Ö','Ô','Ò','Ó'] => 'O',
    ['ú','ù','û','ü'] => 'u',
    ['Ú','Û','Ù','Ü'] => 'U',
    ['ç'] => 'c', ['Ç'] => 'C',
    ['ñ'] => 'n', ['Ñ'] => 'N'
  }
  accents.each do |ac,rep|
    ac.each do |s|
      str = str.gsub(s, rep)
    end
  end
  str = str.gsub(/[^a-zA-Z0-9\.,;:\- \'\"\)\(\/\|\&\?\!]/,"")
  str = str.gsub(/[ ]+/," ")
  str = str.gsub(/&amp;/, "&")
  str = str.gsub(/&gt;/, ">")
  str.strip
end

doc = Nokogiri::HTML(html)
doc.search('a').each do |a|
  if a.inner_html =~ /more<b>/ then
    local_url = a['href'].strip
    if local_url
      #workaround for nymag.com's javascript generated print pages
      if local_url =~ /nymag.com\/print\/?\//
        local_url = local_url.gsub("/print/?/", "/")
      end
      local_html = fetch(local_url, a['href'])
      if local_html
        local_doc = Nokogiri::HTML(local_html)
        local_title = local_doc.search('title').inner_html
        #cheat due to lack of unicode gem (or lack of intelligence on my part - LC)
        local_title = tidy_title(local_title)
        begin
          record = {'link' => a['href'], 'title' => local_title}
          ScraperWiki.save(['link'], record)
        rescue
          raise local_title.inspect
        end
      end
    end
  end
end
