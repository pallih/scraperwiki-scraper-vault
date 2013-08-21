require 'nokogiri'           
html = ScraperWiki::scrape("http://www.parliament.uk/edm/2012-13/5560/peter-aldous")           

doc = Nokogiri::HTML html

counter = 0

doc.search("table#topic-list tbody tr td a").each do |v|
  
  if (counter % 2) == 1
    data = {
      title: v.content,
      href: v['href']
    }
    
    puts data.to_json

    ScraperWiki::save_sqlite(['title'], data)   

  end

  counter = counter + 1

end


