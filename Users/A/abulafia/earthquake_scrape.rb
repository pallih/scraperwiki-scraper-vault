require 'nokogiri'

MAPPING = {
  "event_id"  => ".//*[@id='parameters']/tr[10]/td",
  "magnitude" => ".//*[@id='parameters']/tr[1]/td/strong",
  "datetime"  => ".//*[@id='parameters']/tr[2]/td/ul/li[1]/strong",
  "location"  => ".//*[@id='parameters']/tr[3]/td"
}


def get(url, parse=true)
  html = ScraperWiki.scrape(url)
  parse ? Nokogiri::HTML(html) : html
end

def extract_data(doc, mapping=MAPPING)
  data = {}
  mapping.each_pair do |key, path|
    data[key] = doc.xpath(path + "/text()")
  end
  data
end

def save(record)
  ScraperWiki.save(['event_id'], record)
end

start_url = "http://earthquake.usgs.gov/earthquakes/eqinthenews/2011/"

list  = get(start_url)
links = list.xpath(".//*[@id='main']/div[2]/ul/li/a/@href")

links.each do |link|
  doc  = get(link)
  data = extract_data(doc)
  data['url'] = link
  save(data) 
end



