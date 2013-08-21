require 'nokogiri'
require 'uri'

def handle_link a, base_uri
  name = a.inner_text
  uri = base_uri.merge(a['href']).to_s

  entry = {
      'lobbying_entity' => name,
      'uri' => uri
  }
  ScraperWiki.save_sqlite(['uri'], entry, 'entries')  
end

uri = 'http://www.appc.org.uk/en/register/current-register.cfm'
base_uri = URI.parse(uri)

html = ScraperWiki.scrape uri
doc = Nokogiri::HTML html

doc.search('.layer-register-list li a').each do |a|
  handle_link(a, base_uri) if a['href']
end