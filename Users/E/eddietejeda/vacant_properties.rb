# Blank Ruby

require 'nokogiri'

for i in 1..318
  
  html = ScraperWiki::scrape("http://zipatlas.com/us/zip-code-comparison/percentage-vacant-housing-units.#{i}.htm")
  doc = Nokogiri::HTML(html)
  
  doc.css('tr').each_with_index do |node, index|
  

    unless node.css('.report_data')[3].nil?  
      order = node.css('.report_data')[0] # For the second
      zipcode = node.css('.report_data')[1] # For the second
      location = node.css('.report_data')[2] # For the second
      city = node.css('.report_data')[3] # For the second
      population = node.css('.report_data')[4] # For the second
      percent_vacant = node.css('.report_data')[5] # For the second
      national_rank = node.css('.report_data')[6] # For the second


      data = {  order: order.content, 
                zipcode: zipcode.content,
                location: location.content,
                city: city.content,
                population: population.content, 
                percent_vacant: percent_vacant.content , 
                national_rank: national_rank.content  }
      #puts data.inspect
      ScraperWiki::save_sqlite(['order', 'zipcode', 'location', 'city', 'population', 'percent_vacant', 'national_rank' ], data)
    end

  
  end

end
