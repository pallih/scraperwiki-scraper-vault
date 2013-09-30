# encoding: utf-8
require 'nokogiri'

Encoding.default_external = 'UTF-8'
Encoding.default_internal = 'UTF-8'



html = ScraperWiki.scrape("http://stortinget.no/no/Stottemeny/Kontakt/Partier-og-representanter/Representantenes-e-postadresser/")
doc = Nokogiri::HTML.parse(html)

doc.css(".mainbody > p").each do |node|
  anchors = node.css("a").to_a
  next if anchors.empty? 
    
  emails = anchors.map(&:text)
  text = node.xpath(".//text()").map(&:text).join(' ')

  p text

  text.scan(/(.+?)\s*,(.+?)\s*(?:,.+?)?\s*[;:,].+?@stortinget\.no/).each_with_index do |names, idx|
    last_name, first_name = names.map { |e| e.strip.gsub("\u00a0", '') }
    email = emails[idx]


    # correct mistakes on page
    case [first_name, last_name]
    when ["Hadja", "Tajik"]
      first_name = "Hadia"
    when ["Torgeir", "Trældahl"]
      last_name = "Trældal"
    end
  
    if first_name == "Fremskrittspartiet"
      last_name, first_name = last_name.split(" ")
    end

    data = {
      "first_name" => first_name.split(" ").first, # intentionally ignore middle names 
      "last_name"  => last_name,
      "email"      => email
    }

    p [idx, data]
  
    ScraperWiki.save_sqlite(["first_name", "last_name"], data)
  end
end



# encoding: utf-8
require 'nokogiri'

Encoding.default_external = 'UTF-8'
Encoding.default_internal = 'UTF-8'



html = ScraperWiki.scrape("http://stortinget.no/no/Stottemeny/Kontakt/Partier-og-representanter/Representantenes-e-postadresser/")
doc = Nokogiri::HTML.parse(html)

doc.css(".mainbody > p").each do |node|
  anchors = node.css("a").to_a
  next if anchors.empty? 
    
  emails = anchors.map(&:text)
  text = node.xpath(".//text()").map(&:text).join(' ')

  p text

  text.scan(/(.+?)\s*,(.+?)\s*(?:,.+?)?\s*[;:,].+?@stortinget\.no/).each_with_index do |names, idx|
    last_name, first_name = names.map { |e| e.strip.gsub("\u00a0", '') }
    email = emails[idx]


    # correct mistakes on page
    case [first_name, last_name]
    when ["Hadja", "Tajik"]
      first_name = "Hadia"
    when ["Torgeir", "Trældahl"]
      last_name = "Trældal"
    end
  
    if first_name == "Fremskrittspartiet"
      last_name, first_name = last_name.split(" ")
    end

    data = {
      "first_name" => first_name.split(" ").first, # intentionally ignore middle names 
      "last_name"  => last_name,
      "email"      => email
    }

    p [idx, data]
  
    ScraperWiki.save_sqlite(["first_name", "last_name"], data)
  end
end



