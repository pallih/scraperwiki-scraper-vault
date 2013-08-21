# encoding: UTF-8

scraper = "scraper"
#scraper = "command-line"

require 'nokogiri'
require 'csv'

require 'open-uri'
require 'json'
html = open("http://en.wikipedia.org/wiki/Right-_and_left-hand_traffic#Jurisdictions_with_right-hand_traffic")

iso_3166_string = open("https://raw.github.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv", :ssl_verify_mode => OpenSSL::SSL::VERIFY_NONE).read
iso_3166_string.gsub!(/\\,/, "")
$country_codes = CSV.parse(iso_3166_string, :headers => true)

def fill_in_country_codes(country, data)
  known_synonyms = { 
    "East Timor" => "Timor-Leste",
    "Burma" => "Myanmar",
    "Congo (Brazzaville)" => "Congo",
    "Congo (Kinshasa)" => "Congo the Democratic Republic of the",
    "Laos" => "Lao People's Democratic Republic",
    "Korea" => "Korea Republic of",
    "North Korea" => "Korea Democratic People",
    "São Tomé and Príncipe" => "Sao Tome and Principe",
    "Vietnam" => "Viet Nam",
  }
  # rename country with synonym, if synonym exists
  country = known_synonyms[country] || country 

  country_code = $country_codes.find{|cc| cc["name"] =~ /#{country}/i }
  if country_code
    [ "alpha-2",
      "alpha-3",
      "country-code",
      "iso_3166-2",
      "region-code",
      "sub-region-code"].each do |code|
        data[code] = country_code[code]
    end
  else
    puts "No country code found for #{country}"
  end
end

doc = Nokogiri::HTML html

{ "left"  => "Jurisdictions_with_left-hand_traffic", 
  "right" => "Jurisdictions_with_right-hand_traffic"}.each do |side, id_name|
  puts "Searching #{side}"
  puts doc.css("span").size
  puts doc.css("span#"+id_name).size
  doc.css("span##{id_name}").each do |span|
    next_div = span.parent.next_sibling.next_sibling
    next_div.css("div.NavContent table tr td p > a").each do |a|
      next if a.inner_text == "details"

      country = a.inner_text
      data = {side: side, country: country }
      fill_in_country_codes(country, data)

      puts(data.to_json)
      ScraperWiki::save_sqlite(['side', 'country'], data) if scraper == "scraper"
    end
  end
end
