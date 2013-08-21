require 'nokogiri'

# hostname part of the url
HOST = "http://notes.leipzig.de"

# mapping of the details html table elements to field names
MAP = {
  'datum'   => '/html/body/form/table[3]/tr[1]/td[2]',
  'uhrzeit' => '/html/body/form/table[3]/tr[2]/td[2]',
  'gremium' => '/html/body/form/table[3]/tr[3]/td[2]',
  'ort'     => '/html/body/form/table[3]/tr[6]/td[2]',
  'strasse' => '/html/body/form/table[3]/tr[7]/td[2]',
  'raum'    => '/html/body/form/table[3]/tr[8]/td[2]'
}

# the unique key(s); used for saving to the datastore
UNIQUE_KEYS = ['datum']

# takes a relative path as argument, returns a Nokogiri document per default, override with 'false' as second argument
def get(path, parse=true)
  url  = HOST + path
  html = ScraperWiki.scrape(url)
  parse ? Nokogiri::HTML(html) : html
end

# takes a nokogiri document of gremium summary and extracts the interesting fields; returns a hash with the data
def extract_data(doc)
  data = {}
  MAP.each_pair {|key, path| data[key] = doc.xpath(path + "//text()").to_s}
  data  
end

# takes a hash and saves it to the datastore
def save(data)
  ScraperWiki.save_sqlite(unique_keys=UNIQUE_KEYS, data)
end

start = "/APPL/LAURA/WP5/kais02.nsf/WebTO_NSAuswahl?OpenView&Start=1&Count=1000&ExpandView&RestrictToCategory=StadtbezirksbeiratLeipzig-West"

list  = get(start)
links = list.xpath("//a[@id='answer']/@href")

links.each do |link|
  doc  = get(link)
  data = extract_data(doc)
  data["url"] = HOST + link
  save(data)
end

# TODO: oeffentlich/nicht-oeffentlich, protokoll-url




