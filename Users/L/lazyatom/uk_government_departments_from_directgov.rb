require 'rubygems'
require 'hpricot'
require 'scraperwiki'

def department_urls_from_letter_page(url)
  page_html = ScraperWiki.scrape(url)
  doc = Hpricot(page_html)
  (doc/".subContent .subLinks a").map do |a|
    if a[:href] =~ /^http/
      a[:href]
    else
      "http://www.direct.gov.uk" + a[:href]
    end
  end
end

def data_from_li(li)
  key = (li/".headingContainer").inner_text.strip
  raw_value = (li/".infoContainer span")
  case key
  when "Contact point"
    {"Name" => raw_value.inner_text.strip}
  when "Email address"
    {key => raw_value.inner_text}
  when "Website (opens new window)"
    {"Website" => raw_value.inner_text}
  when "Phone number"
    if (types = (raw_value/"strong")).any? 
      ary = raw_value.inner_html.split("<br />").map { |s| s.gsub("<strong>", "").gsub("</strong>", "") }
      numbers = types.map do |t|
        type_text = t.inner_text
        number =  ary[ary.index(type_text)+1]
        [type_text, number]
      end
      {key => numbers}
    else
      {key => raw_value.inner_text}
    end
  when "Address"
    cleaned_value = raw_value.inner_html.split("<br />")
    postcode = cleaned_value.pop
    puts postcode
    lat, lng = ScraperWiki.gb_postcode_to_latlng(postcode)
    {key => cleaned_value.join(", "), "Postcode" => postcode, "Latitude" => lat, "Longitude" => lng}
  else
    cleaned_value = raw_value.inner_html.gsub("<br />", "\n")
    {key => cleaned_value}
  end
end 

def organisation_data_from_page(url)
  page_html = ScraperWiki.scrape(url)
  doc = Hpricot(page_html)
  data_elements = doc/".contactsInfo li"
  data_elements.inject({}) do |h, li|
    h.merge(data_from_li(li))
  end
end

def store(data)
  if data["Name"]
    ScraperWiki.save_sqlite(["Name"], data)
  else
    puts "Cannot store: #{data.inspect}"
  end
end

letters = "A".."Z"

letters.each do |letter|
  url = "http://www.direct.gov.uk/en/Dl1/Directories/A-ZOfCentralGovernment/index.htm?indexChar=#{letter}"
  department_urls = department_urls_from_letter_page(url)
  department_urls.each do |organisation_url|
    data = organisation_data_from_page(organisation_url)
    store(data.merge("Source URL" => organisation_url))
  end
end
require 'rubygems'
require 'hpricot'
require 'scraperwiki'

def department_urls_from_letter_page(url)
  page_html = ScraperWiki.scrape(url)
  doc = Hpricot(page_html)
  (doc/".subContent .subLinks a").map do |a|
    if a[:href] =~ /^http/
      a[:href]
    else
      "http://www.direct.gov.uk" + a[:href]
    end
  end
end

def data_from_li(li)
  key = (li/".headingContainer").inner_text.strip
  raw_value = (li/".infoContainer span")
  case key
  when "Contact point"
    {"Name" => raw_value.inner_text.strip}
  when "Email address"
    {key => raw_value.inner_text}
  when "Website (opens new window)"
    {"Website" => raw_value.inner_text}
  when "Phone number"
    if (types = (raw_value/"strong")).any? 
      ary = raw_value.inner_html.split("<br />").map { |s| s.gsub("<strong>", "").gsub("</strong>", "") }
      numbers = types.map do |t|
        type_text = t.inner_text
        number =  ary[ary.index(type_text)+1]
        [type_text, number]
      end
      {key => numbers}
    else
      {key => raw_value.inner_text}
    end
  when "Address"
    cleaned_value = raw_value.inner_html.split("<br />")
    postcode = cleaned_value.pop
    puts postcode
    lat, lng = ScraperWiki.gb_postcode_to_latlng(postcode)
    {key => cleaned_value.join(", "), "Postcode" => postcode, "Latitude" => lat, "Longitude" => lng}
  else
    cleaned_value = raw_value.inner_html.gsub("<br />", "\n")
    {key => cleaned_value}
  end
end 

def organisation_data_from_page(url)
  page_html = ScraperWiki.scrape(url)
  doc = Hpricot(page_html)
  data_elements = doc/".contactsInfo li"
  data_elements.inject({}) do |h, li|
    h.merge(data_from_li(li))
  end
end

def store(data)
  if data["Name"]
    ScraperWiki.save_sqlite(["Name"], data)
  else
    puts "Cannot store: #{data.inspect}"
  end
end

letters = "A".."Z"

letters.each do |letter|
  url = "http://www.direct.gov.uk/en/Dl1/Directories/A-ZOfCentralGovernment/index.htm?indexChar=#{letter}"
  department_urls = department_urls_from_letter_page(url)
  department_urls.each do |organisation_url|
    data = organisation_data_from_page(organisation_url)
    store(data.merge("Source URL" => organisation_url))
  end
end
