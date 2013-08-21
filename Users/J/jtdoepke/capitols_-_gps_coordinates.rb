require 'nokogiri'

data = Array.new

par = Nokogiri::HTML(ScraperWiki.scrape("https://www.cia.gov/library/publications/the-world-factbook/index.html"))

country_codes = Array.new

for node in par.search("select[@name='countryCode']").search("option")
  d = node.attribute("value").to_s
  if not d.empty? 
    country_codes << d
  end
end


for country in country_codes
  par = Nokogiri::HTML(ScraperWiki.scrape("https://www.cia.gov/library/publications/the-world-factbook/geos/"+country+".html")).at_css("body")
  d = {:country_code => country}
  x = par.at_css('div[@class="region1"]')
  if not x.nil? 
    par.xpath("//div[@class='region1']/a").first.content
    d[:region] = x.xpath("//div[@class='region1']/a").first.content.to_s
    d[:country] = x.at_css("span[@class='region_name1']").content.to_s
    puts capital_root = par.xpath('//div[@class="category"]/a[@alt="Definitions and Notes: Capital"]/../../..').first
    puts capital_name = capital_root.next_element
    data << d
    puts d.to_json
  end
end