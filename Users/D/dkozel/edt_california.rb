require 'uri'
require 'nokogiri'




def scrape_zip (zip)

  html = ScraperWiki.scrape('http://www.ebt.ca.gov/caebtclient/cashlocationSearch.recip;jsessionid=B8C369A34BEDCF58CAB6AD5F6A7078FF?org.apache.struts.taglib.html.TOKEN=fd795405e2c60b492e3e5cab8287647a&zip='+ zip +'&city=&searchType=0&name=&count=0&startIndex=0')
 doc = Nokogiri::HTML(html)

  for v in doc.css('tr.RowOdd')
    cells = v.search('td')
    data = {
      'name' => cells[0].inner_html,
      'address' => cells[1].inner_html,
      'city' => cells[2].inner_html,
      'state' => cells[3].inner_html,
      'zip' => cells[4].inner_text,
      'restaurant_meals' => cells[5].inner_html,
      'farmers_market' => cells[6].inner_html
    }
    ScraperWiki.save(["address"], data)
    puts data
  end
end

i = 0

for i in (90000..96162)
  puts i
  scrape_zip i.to_s()
endrequire 'uri'
require 'nokogiri'




def scrape_zip (zip)

  html = ScraperWiki.scrape('http://www.ebt.ca.gov/caebtclient/cashlocationSearch.recip;jsessionid=B8C369A34BEDCF58CAB6AD5F6A7078FF?org.apache.struts.taglib.html.TOKEN=fd795405e2c60b492e3e5cab8287647a&zip='+ zip +'&city=&searchType=0&name=&count=0&startIndex=0')
 doc = Nokogiri::HTML(html)

  for v in doc.css('tr.RowOdd')
    cells = v.search('td')
    data = {
      'name' => cells[0].inner_html,
      'address' => cells[1].inner_html,
      'city' => cells[2].inner_html,
      'state' => cells[3].inner_html,
      'zip' => cells[4].inner_text,
      'restaurant_meals' => cells[5].inner_html,
      'farmers_market' => cells[6].inner_html
    }
    ScraperWiki.save(["address"], data)
    puts data
  end
end

i = 0

for i in (90000..96162)
  puts i
  scrape_zip i.to_s()
end