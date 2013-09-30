require 'rubygems'
require 'nokogiri'
require 'open-uri'

scraped_links = Array.new
destinations = [ "western_mediterranean" , "eastern_mediterranean" , "atlantic_ocean" ]

destinations.each { |destination|
  for i in 1..9 do
    page = Nokogiri::HTML(open("http://www.costacruises.co.uk/gb/cruises_list/"+destination+"-20130"+i.to_s()+".html"))

    cruise_href = page.xpath("//a[contains(@href, 'cruise_details')]")

    cruise_href.each do |href|
      address = href["href"]
      scraped_links.push("http://www.costacruises.co.uk" + address.dup)
    end
  end

  for i in 10..12 do
    page = Nokogiri::HTML(open("http://www.costacruises.co.uk/gb/cruises_list/"+destination+"-2013"+i.to_s()+".html"))

    cruise_href = page.xpath("//a[contains(@href, 'cruise_details')]")

    cruise_href.each do |href|
      address = href["href"]
      scraped_links.push("http://www.costacruises.co.uk" + address.dup)
    end
  end
}

scraped_links.each do  |url|
  scraped_link = Nokogiri::HTML(open(url))
  depdate = scraped_link.xpath("//td[./@class='departures']")
  depdate.each do |sailing|
    cruises = {}
    
    cruises[:departure] = sailing.text()
    cruises[:website] = url.to_s()      
    cruises[:inside] = sailing.xpath("//span[./@id='ctl00_cph_PageContent_rptDD_ctl01_rpDDBS_ctl00_lblPrice']").text()[5..-1]
    cruises[:outside] = sailing.xpath("//span[./@id='ctl00_cph_PageContent_rptDD_ctl01_rpDDBS_ctl01_lblPrice']").text()[5..-1]
    cruises[:balcony] = sailing.xpath("//span[./@id='ctl00_cph_PageContent_rptDD_ctl01_rpDDBS_ctl02_lblPrice']").text()[5..-1]
    cruises[:minisuite] = sailing.xpath("//span[./@id='ctl00_cph_PageContent_rptDD_ctl01_rpDDBS_ctl03_lblPrice']").text()[5..-1]
    
    ports = scraped_link.xpath("//a[contains(@id, 'PortName')]/text()").to_a().join(";")
    cruises[:ports_of_call] = ports

    ScraperWiki::save_sqlite(["departure"], cruises, "CostaCruises", 0)
    #price = "#{val};#{inside[5..-1]};#{outside[5..-1]};#{balcony[5..-1]};#{minisuite[5..-1]}"
    #output.push(price.dup)
  end
end

#puts output
require 'rubygems'
require 'nokogiri'
require 'open-uri'

scraped_links = Array.new
destinations = [ "western_mediterranean" , "eastern_mediterranean" , "atlantic_ocean" ]

destinations.each { |destination|
  for i in 1..9 do
    page = Nokogiri::HTML(open("http://www.costacruises.co.uk/gb/cruises_list/"+destination+"-20130"+i.to_s()+".html"))

    cruise_href = page.xpath("//a[contains(@href, 'cruise_details')]")

    cruise_href.each do |href|
      address = href["href"]
      scraped_links.push("http://www.costacruises.co.uk" + address.dup)
    end
  end

  for i in 10..12 do
    page = Nokogiri::HTML(open("http://www.costacruises.co.uk/gb/cruises_list/"+destination+"-2013"+i.to_s()+".html"))

    cruise_href = page.xpath("//a[contains(@href, 'cruise_details')]")

    cruise_href.each do |href|
      address = href["href"]
      scraped_links.push("http://www.costacruises.co.uk" + address.dup)
    end
  end
}

scraped_links.each do  |url|
  scraped_link = Nokogiri::HTML(open(url))
  depdate = scraped_link.xpath("//td[./@class='departures']")
  depdate.each do |sailing|
    cruises = {}
    
    cruises[:departure] = sailing.text()
    cruises[:website] = url.to_s()      
    cruises[:inside] = sailing.xpath("//span[./@id='ctl00_cph_PageContent_rptDD_ctl01_rpDDBS_ctl00_lblPrice']").text()[5..-1]
    cruises[:outside] = sailing.xpath("//span[./@id='ctl00_cph_PageContent_rptDD_ctl01_rpDDBS_ctl01_lblPrice']").text()[5..-1]
    cruises[:balcony] = sailing.xpath("//span[./@id='ctl00_cph_PageContent_rptDD_ctl01_rpDDBS_ctl02_lblPrice']").text()[5..-1]
    cruises[:minisuite] = sailing.xpath("//span[./@id='ctl00_cph_PageContent_rptDD_ctl01_rpDDBS_ctl03_lblPrice']").text()[5..-1]
    
    ports = scraped_link.xpath("//a[contains(@id, 'PortName')]/text()").to_a().join(";")
    cruises[:ports_of_call] = ports

    ScraperWiki::save_sqlite(["departure"], cruises, "CostaCruises", 0)
    #price = "#{val};#{inside[5..-1]};#{outside[5..-1]};#{balcony[5..-1]};#{minisuite[5..-1]}"
    #output.push(price.dup)
  end
end

#puts output
