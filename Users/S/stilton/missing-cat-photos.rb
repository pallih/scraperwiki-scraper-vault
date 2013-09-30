# Missing cats register

require 'nokogiri'

html = ScraperWiki.scrape("http://www.nationalpetregister.org/mp-cats.php")
puts html

# Find the photos of the cats!
#<li class="pet_results_photo"><a href="mp/27945.htm" title="Missing Cat in Selby Avenue South Shore"><img src="http://www.nationalpetregister.org/photos/20111235709.jpg" alt="Missing Cats in Selby Avenue South Shore" border="0" width="64" height="48"></a></li>

doc = Nokogiri::HTML(html)
doc.search('.pet_results').each do |item|
  img = item.search('.pet_results_photo img')[0]
  data = {
    'id' => item.search('.pet_results_id')[0].content.to_i,
    'photo' => img['src'],
    'title' => img['alt']
  }
  puts data
  ScraperWiki.save(unique_keys=['id',], data)
end

# Missing cats register

require 'nokogiri'

html = ScraperWiki.scrape("http://www.nationalpetregister.org/mp-cats.php")
puts html

# Find the photos of the cats!
#<li class="pet_results_photo"><a href="mp/27945.htm" title="Missing Cat in Selby Avenue South Shore"><img src="http://www.nationalpetregister.org/photos/20111235709.jpg" alt="Missing Cats in Selby Avenue South Shore" border="0" width="64" height="48"></a></li>

doc = Nokogiri::HTML(html)
doc.search('.pet_results').each do |item|
  img = item.search('.pet_results_photo img')[0]
  data = {
    'id' => item.search('.pet_results_id')[0].content.to_i,
    'photo' => img['src'],
    'title' => img['alt']
  }
  puts data
  ScraperWiki.save(unique_keys=['id',], data)
end

