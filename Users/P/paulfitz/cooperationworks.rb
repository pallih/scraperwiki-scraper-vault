require 'json'
require 'nokogiri'           

html = ScraperWiki::scrape("http://www.cooperationworks.coop/")           
html =~ /("markers": .*)\} \} \}/
code = $1
code.gsub!("\\x3c","<")
code.gsub!("\\x3e",">")
p code
markers = JSON.parse("{#{code}}")
markers = markers["markers"]
markers.each do |marker|
  txt = marker["text"]
  doc = Nokogiri::HTML(txt)
  address1 = nil
  city = nil
  state = nil
  zip = nil
  email = nil
  doc.search("div[@class='views-field-address'] div[@class='adr']").each do |v|
    address1 = v.search("div[@class='street-address']/text()")[0]
    city = v.search("span[@class='locality']/text()")[0]
    state = v.search("span[@class='region']/text()")[0]
    zip = v.search("span[@class='postal-code']/text()")[0]
  end
  email = doc.search("div[@class='views-field-field-mem-location-email-email'] span[@class='field-content'] a/text()")[0]
  website = doc.search("div[@class='views-field-field-org-mem-website-url'] span[@class='field-content'] a/@href")[0]
  doc.search("div[@class='views-field-title'] span[@class='field-content'] a").each do |v|
    name = v.inner_html
    data = {
      'name' => name,
      'latitude' => marker["latitude"],
      'longitude' => marker["longitude"],
      'address1' => address1,
      'city' => city,
      'state' => state,
      'zip' => zip,
      'email' => email,
      'website' => website
    }
    ScraperWiki::save_sqlite(['name'], data)
  end
end
