require 'json'
require 'open-uri'

def get_json uri
  begin
    json = open(uri).read
    JSON.parse(json)
  rescue
    retry
  rescue Timeout::Error
    retry
  end
end

uri = 'http://iatiregistry.org/api/rest/package'
list = get_json uri

list.each do |item|
  uri = "http://iatiregistry.org/api/rest/package/#{item}"
  data = get_json uri
  if data
    record = {
      'download_url' => data['download_url'],
      'ckan_url' => data['ckan_url'],
      'title' => data['title'],
      'activity_period-from' => data['extras']['activity_period-from'],
      'activity_period-to' => data['extras']['activity_period-to']
    }
  
    ScraperWiki.save(['download_url'], record)
  end
endrequire 'json'
require 'open-uri'

def get_json uri
  begin
    json = open(uri).read
    JSON.parse(json)
  rescue
    retry
  rescue Timeout::Error
    retry
  end
end

uri = 'http://iatiregistry.org/api/rest/package'
list = get_json uri

list.each do |item|
  uri = "http://iatiregistry.org/api/rest/package/#{item}"
  data = get_json uri
  if data
    record = {
      'download_url' => data['download_url'],
      'ckan_url' => data['ckan_url'],
      'title' => data['title'],
      'activity_period-from' => data['extras']['activity_period-from'],
      'activity_period-to' => data['extras']['activity_period-to']
    }
  
    ScraperWiki.save(['download_url'], record)
  end
end