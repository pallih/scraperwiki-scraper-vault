# Blank Ruby
require 'nokogiri'
require 'open-uri'
doc = Nokogiri::HTML(open('http://www.tinydeal.com/android-phones-c-54_678_790.html?pagesize=100&disp_order=18&pfrom=100&pto=149&is_input=1&inc_subcat=1&keyword=MTK6577'))

url = 'tinydeal.com'

count = 0
for el in doc.css('li.productListing-even') 
  count = count + 1
  puts el
  serial_content = el.at_css('a.p_box_title').content
  puts serial_content 
  vendor = serial_content.split[0].sub("(","").sub(")","").capitalize
  model = serial_content.split[1]

  pcontent = el.at_css('div.p_box_price').content.split("$")[1]
  price_content = (pcontent+"F").split("F")[0]
  puts price_content 

  listing = {
    serial: serial_content,
    vendor: vendor,
    model: model,
    url: url,
    price: price_content
  }
  ScraperWiki::save_sqlite(['serial'], listing)

end

# Blank Ruby
