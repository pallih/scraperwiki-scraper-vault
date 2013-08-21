require 'nokogiri'
require 'open-uri'
require 'scraperwiki'
require 'stringex'

def offer_exists?(d)
  d.search("p").size > 1
end

def offer_void?(d)
  d.search("p").size == 0
end

def last_offer_id()
  a = ScraperWiki::select("max(id) as loi from swdata")
  puts "last_offer_id: #{a}"
  a[0]['loi'].to_i
end

def scrape_offer(id)
  data = {}
  data['id'] = id
  html = ScraperWiki::scrape("http://www.up.warszawa.pl/oferty/strony/szczegol_of.php?id=#{id}")
  html.force_encoding("UTF-8")
  d = Nokogiri::HTML(html)
  
  return false unless offer_exists?(d) || offer_void?(d)
  
  d.search("p").each_with_index do |e, i|
    if i == 0
      a = e.text.match /nr: (\S+) z dnia (\S+)/
      data['number'] = a[1]
      data['day'] = a[2]
    else    
      a = e.text.strip.split(':')
      #data[a[0].force_encoding('US-ASCII')] = a[1] || ''
      data[a[0].to_ascii.strip] = (a[1] || '').strip
    end
  end

  ScraperWiki::save(["id"], data, Time.now) unless offer_void?(d)
  #p data
  true
end

def run
  #scrape_offer(12938)
  loi = last_offer_id + 1
  (0..100).each do |i|
    id = loi + i
    puts "getting offer id: #{id}"
    break unless scrape_offer(id)
  end  
end

run


