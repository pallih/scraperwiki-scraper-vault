# Blank Ruby

puts "hello, ruby to the cloud "

html = ScraperWiki.scrape("http://www.afdc.energy.gov/afdc/laws/matrix/tech")
puts html




require 'nokogiri'
doc = Nokogiri::HTML(html)

doc.css('div.featured a').each do |link|
  puts link.class
end

for v in doc.search('matrix')
  cells = v.search('td')
  data = {
    'Jurisdiction'           => cells[0].inner_html,
    'Biodiesel'              => cells[1].inner_html.to_i,
    'Ethanol'                => cells[2].inner_html.to_i,
    'NaturalGas'             => cells[3].inner_html.to_i,
    'LPG'                    => cells[4].inner_html.to_i,
    'Hydrogen'               => cells[5].inner_html.to_i,
    'Ev'                     => cells[5].inner_html.to_i,
    'HEV'                    => cells[6].inner_html.to_i,
    'NEV'                    => cells[7].inner_html.to_i,
    'AfterMarketConversions' => cells[8].inner_html.to_i,
    'FuelEcoOrEffiency'      => cells[9].inner_html.to_i,
    'IdleReduction'          => cells[10].inner_html.to_i,
    'Other'                  => cells[11].inner_html.to_i
 
  }
  puts data.to_json
end


ScraperWiki.save_sqlite(unique_keys=['Jurisdiction'], data=data)           

#select * from swdata order by Jurisdiction desc limit 10

for el in doc.css('html').children           
    puts el.name
    for el2 in el.children
        puts "--" + el2.name + " " + el2.attributes.to_json
    end
end