require 'nokogiri'

require 'open-uri'

BASE_URL = 'http://www.edinburgh.gov.uk/' 
BASE_SCRAPE_URL = BASE_URL + 'directory/49/a_to_z/'

# scrapes a detail page (details for one eating establishment)
# a detail page has HTML that looks something like this
# <table class="directoryRecord"> 
# <tr><th>Name</th><td>Auld Hoose</td></tr>  <!-- 0 -->
# <tr><th>Address</th><td>23-25  St Leonard&#039;s Street</td></tr>  <!-- 1 -->
# <tr><th>Postcode</th><td>EH8 9QN</td></tr>  <!-- 2 -->
# <tr><th>Location</th><td><input type="hidden" id="map_marker_image_640" value="http://www.edinburgh.gov.uk/site/images/map_markers/red.png" />
#   <input type="hidden" id="map_marker_info_640" value="" />
#   <input type="hidden" id="map_marker_location_640" value="55.943376,-3.180138" />
#   <div id="map_640" class="googleMap" style="border:1px solid #D1D1D1; height:250px; width:550px;">
#   </div></td></tr>
# <tr><th>Last inspection date</th><td>10/07/2009</td></tr>
# <tr><th>Rating</th><td>Improvement Required</td></tr> 
# </table>
def scrape_detail_page (detail_name, detail_url)
  html = ScraperWiki.scrape(detail_url)
  doc = Nokogiri::HTML(html)
  #doc = Nokogiri::HTML(open(detail_url))  #testing
  #doc = Nokogiri::HTML(File.open('data'))  #testing
  rows = doc.xpath('//table[@class="directoryRecord"]/tr')  
  record = {}
  record['name'] = detail_name
  record['url'] = detail_url
  record['address'] = ''
  record['postcode'] = ''
  record['lat'] = ''
  record['long'] = ''
  record['inspection_date'] = ''
  record['rating'] = ''

   if rows.nil? 
     puts "EMPTY!!!!"
   end

  if !rows.nil? 
  rows.each do |r|
    case r.xpath('th').text
      when "Name"
        record['name'] = r.xpath('td').text
      when "Address"
        record['address'] = r.xpath('td').text
      when "Postcode"
        record['postcode'] = r.xpath('td').text
      when "Location"
        coords = r.xpath('td//input')[2]["value"]
        if !coords.nil? 
           cs = coords.split(',')
           lat = cs[0]
           long = cs[1]
           record['lat'] = lat
           record['long'] = long
        end
      when "Last inspection date"
        record['inspection_date'] = r.xpath('td').text
      when "Rating"  
        record['rating'] = r.xpath('td').text
    end #case
                                                                                                                                                                                                                                                                                                                                                                                                                     end #rows
  end #if
  ScraperWiki.save(['name','url'], record)
end

# 
# html = ScraperWiki.scrape(starting_url)
# 
# # use Nokogiri to get all <td> tags
# doc = Nokogiri::HTML(html)
# doc.search('td').each do |td|
#     puts td.inner_html
#     record = {'td' => td.inner_html}
#     ScraperWiki.save(['td'], record)
# end



# scrapes a listing page (one letter of the alphabet)
def scrape_listing_page (url) 
  html = ScraperWiki.scrape(url)
  doc = Nokogiri::HTML(html)
  doc.xpath('//ul[@class="listBulletArrow"]/li/a').each do |link|
    detail_url = BASE_URL + link["href"]
    detail_name = link.content
    scrape_detail_page(detail_name, detail_url)
  end 
end  

def scrape_all
  #alphabet = %w{a b c d e f g h i j k l m n o p q r s t u v w x y z}
  alphabet = %w{c}  #we just do those restaurants starting with "c" to save irritation...
  alphabet.each do |char|
   url_to_scrape = BASE_SCRAPE_URL + char
   scrape_listing_page(url_to_scrape)
  end
end

scrape_all
#scrape_detail_page('xxx', BASE_URL + 'directory_record/13132/creelers')
#scrape_listing_page(BASE_SCRAPE_URL + 'c')