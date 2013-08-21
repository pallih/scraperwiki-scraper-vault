# Blank Ruby

html = ScraperWiki.scrape "http://www.menupages.com/restaurants/all-areas/all-neighborhoods/american-new"

base_url = "http://www.menupages.com"

require 'nokogiri'

rest_array = []
@menu_array = []

def nokogiri(html)
  Nokogiri::HTML(html)
end

#scrape menu function
def scrape_page(url)
  menu_html = ScraperWiki.scrape(url)
  menu_doc = nokogiri(menu_html)
  menu_doc.css('div#restaurant-menu h3, table.price-three th').each do |link|
    
    ScraperWiki.save([:data], {data: link.inner_html})
  end
end 


#Start Here
doc = nokogiri(html)
doc.css('td.name-address a.link').each do |link|
  rest_array << link['href']
end

p rest_array

#Go through the menu links
rest_array.each do |rest_link|
  next_menu_link = base_url + rest_link + "menu"
  scrape_page(next_menu_link)
end

p @menu_array


#doc.css('td.name-address a.link').each do |link|
#  ScraperWiki.save([:data], {data: link['href']})
#end


