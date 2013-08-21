require 'mechanize'
require 'nokogiri'
require 'uri'

def handle_item item
  wikipedia_uri = item['url']
  page_name = wikipedia_uri.split('/').last
  page = Wikipedia.find(page_name)
  
  website_uri = nil

  if page && (external_uri = page.external_website_uri)
    match = external_uri.detect {|x| ((x.size > 1) && x[1] && x[1][/official/i]) || ((x.size > 2) && x[2] && x[2][/official/i]) }
    unless match
      match = external_uri.detect {|x| ((x.size > 1) && x[1] && x[1][/website/i]) || ((x.size > 2) && x[2] && x[2][/website/i]) }
    end
    website_uri = match.first if match
  end

  ScraperWiki.save(['uri'], {'name' => item['name'], 'uri' => wikipedia_uri, 'website_uri' => website_uri })
  nil
end

uri = 'https://gist.github.com/raw/887730/3263d95655e56db20d07d424380c450ef209ee10/gistfile1.txt'
eval(Mechanize.new.get(uri).body)

ScraperWiki.attach('uk_government_departments_1') 
begin
  ScraperWiki.select('* from `uk_government_departments_1`.swdata').each do |item|
    handle_item(item)
  end
rescue Exception => e
  puts e.to_s
end
