###############################################################################
# Philly Open311 Knowledgebase Scraper
###############################################################################

require 'nokogiri'
require "net/http"
require "uri"

def getUrl(urlStr)
  uri = URI.parse(urlStr)
  http = Net::HTTP.new(uri.host, uri.port)
  request = Net::HTTP::Get.new(uri.request_uri)  
  response = http.request(request)
  return response
end

for i in 506..6700
  # retrieve a page
  base_url = 'http://philly311.phila.gov/default.asp?SID=&Lang=1&id='+i.to_s
  
  resp = getUrl(base_url)

  if resp.code == "200"
    record = {}

    doc = Nokogiri::HTML(resp.body)
    record['id'] = i
    record['question'] = doc.css('td.shortTitle').children.first.inner_text
    record['answer'] = doc.css('table#Table5 td.content').inner_html
    record['modified_date'] = doc.css('td.articledata').inner_text
    record['url'] = base_url.to_s
    # Print out the data we've gathered
    puts record
    # Finally, save the record to the datastore - 'Artist' is our unique key
    ScraperWiki.save(["id"], record)
  end
end
###############################################################################
# Philly Open311 Knowledgebase Scraper
###############################################################################

require 'nokogiri'
require "net/http"
require "uri"

def getUrl(urlStr)
  uri = URI.parse(urlStr)
  http = Net::HTTP.new(uri.host, uri.port)
  request = Net::HTTP::Get.new(uri.request_uri)  
  response = http.request(request)
  return response
end

for i in 506..6700
  # retrieve a page
  base_url = 'http://philly311.phila.gov/default.asp?SID=&Lang=1&id='+i.to_s
  
  resp = getUrl(base_url)

  if resp.code == "200"
    record = {}

    doc = Nokogiri::HTML(resp.body)
    record['id'] = i
    record['question'] = doc.css('td.shortTitle').children.first.inner_text
    record['answer'] = doc.css('table#Table5 td.content').inner_html
    record['modified_date'] = doc.css('td.articledata').inner_text
    record['url'] = base_url.to_s
    # Print out the data we've gathered
    puts record
    # Finally, save the record to the datastore - 'Artist' is our unique key
    ScraperWiki.save(["id"], record)
  end
end
