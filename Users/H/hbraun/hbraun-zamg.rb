# zamg wetter - morgen

require 'nokogiri'    

def extract(url)
  puts url
  html = ScraperWiki::scrape(url)
  doc = Nokogiri::HTML html
  doc.search("div[@id='contMain'] table").each do |v|
    cells = v.search 'td'
    data = {
      day: File.basename(url),
      desc: cells[3].content()
    }
    puts data
    data.to_json
    ScraperWiki::save_sqlite(['day'], data)
    break
  end
end

days = ["http://www.zamg.ac.at/wetter/prognose/index.php",
        "http://www.zamg.ac.at/wetter/prognose/morgen.php",
        "http://www.zamg.ac.at/wetter/prognose/uebermorgen.php"]

days.each do |url| 
  extract url
end


# zamg wetter - morgen

require 'nokogiri'    

def extract(url)
  puts url
  html = ScraperWiki::scrape(url)
  doc = Nokogiri::HTML html
  doc.search("div[@id='contMain'] table").each do |v|
    cells = v.search 'td'
    data = {
      day: File.basename(url),
      desc: cells[3].content()
    }
    puts data
    data.to_json
    ScraperWiki::save_sqlite(['day'], data)
    break
  end
end

days = ["http://www.zamg.ac.at/wetter/prognose/index.php",
        "http://www.zamg.ac.at/wetter/prognose/morgen.php",
        "http://www.zamg.ac.at/wetter/prognose/uebermorgen.php"]

days.each do |url| 
  extract url
end


