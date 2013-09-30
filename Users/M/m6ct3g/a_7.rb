# Blank Ruby
require 'rubygems'  
 require 'nokogiri'  
 require 'open-uri' 
 require 'mechanize'


dests = ["AF",
"AL",
"DZ",
"AO",
"AG",
"AR",
"AM",
"AW",
"AU",
"AT",
"AZ",
"BS",
"BH",
"BD",
"BB",
"BY",
"BE",
"BZ",
"BJ",
"BM",
"BO",
"BQ",
"BA",
"BR",
"BN",
"BG",
"BF",
"BI",
"KH",
"CM",
"CA",
"CV",
"KY",
"TD",
"CL",
"CN",
"TW",
"CO",
"CG",
"CK",
"CR",
"CI",
"HR",
"CU",
"CW",
"CY",
"CZ",
"CD",
"DK",
"DJ",
"DO",
"EC",
"EG",
"SV",
"GQ",
"ER",
"EE",
"ET",
"FJ",
"FI",
"FR",
"PF",
"GA",
"GM",
"GE",
"DE",
"GH",
"GR",
"GD",
"GP",
"GU",
"GT",
"GN",
"GW",
"HT",
"HN",
"HK",
"HU",
"IS",
"IN",
"ID",
"IR",
"IQ",
"IE",
"IL",
"IT",
"JM",
"JP",
"JE",
"JO",
"KZ",
"KE",
"KR",
"KP",
"KW",
"KG",
"LA",
"LV",
"LB",
"LR",
"LY",
"LT",
"LU",
"MO",
"MK",
"MW",
"MY",
"MV",
"ML",
"MT",
"MH",
"MQ",
"MR",
"MU",
"MX",
"FM",
"MD",
"MN",
"ME",
"MA",
"MZ",
"MM",
"NA",
"NP",
"NL",
"NC",
"NZ",
"NI",
"NE",
"NG",
"NU",
"NF",
"MP",
"NO",
"OM",
"PK",
"PW",
"PA",
"PY",
"PE",
"PH",
"PL",
"PT",
"PR",
"QA",
"RO",
"RU",
"RW",
"KN",
"LC",
"WS",
"ST",
"SA",
"SN",
"RS",
"SC",
"SL",
"SG",
"SX",
"SK",
"SI",
"SO",
"ZA",
"SS",
"ES",
"LK",
"SD",
"SE",
"CH",
"SY",
"TJ",
"TZ",
"TH",
"TG",
"TO",
"TT",
"TN",
"TR",
"TM",
"TC",
"UG",
"UA",
"AE",
"GB",
"US",
"UY",
"UZ",
"VU",
"VE",
"VN",
"VI",
"YE",
"ZM",
"ZW"]



flight = {}


dests.each do |dest|
puts "scrape #{dest}"

begin

html = ScraperWiki.scrape("http://www.staralliance.com/destination_overview1.do?language=en&method=fetchAirports&country=#{dest}")

doc = Nokogiri::HTML(html)

row = doc.xpath("//table[@class='avadaytable']/tbody/tr")[0]

rescue

 puts "Something wrong"

end

unless row == nil
price = row.xpath("td[9]/div/label")
dep = row.xpath("td[1]/div")

time = Time.new

puts time.inspect
puts dep.inner_html
puts price.inner_html

flight = {}
flight['time'] = time.inspect
flight['from'] = departure
flight['dest'] = dest


ScraperWiki.save(["time"], flight)

sleep 2



end
end
end
end
# Blank Ruby
require 'rubygems'  
 require 'nokogiri'  
 require 'open-uri' 
 require 'mechanize'


dests = ["AF",
"AL",
"DZ",
"AO",
"AG",
"AR",
"AM",
"AW",
"AU",
"AT",
"AZ",
"BS",
"BH",
"BD",
"BB",
"BY",
"BE",
"BZ",
"BJ",
"BM",
"BO",
"BQ",
"BA",
"BR",
"BN",
"BG",
"BF",
"BI",
"KH",
"CM",
"CA",
"CV",
"KY",
"TD",
"CL",
"CN",
"TW",
"CO",
"CG",
"CK",
"CR",
"CI",
"HR",
"CU",
"CW",
"CY",
"CZ",
"CD",
"DK",
"DJ",
"DO",
"EC",
"EG",
"SV",
"GQ",
"ER",
"EE",
"ET",
"FJ",
"FI",
"FR",
"PF",
"GA",
"GM",
"GE",
"DE",
"GH",
"GR",
"GD",
"GP",
"GU",
"GT",
"GN",
"GW",
"HT",
"HN",
"HK",
"HU",
"IS",
"IN",
"ID",
"IR",
"IQ",
"IE",
"IL",
"IT",
"JM",
"JP",
"JE",
"JO",
"KZ",
"KE",
"KR",
"KP",
"KW",
"KG",
"LA",
"LV",
"LB",
"LR",
"LY",
"LT",
"LU",
"MO",
"MK",
"MW",
"MY",
"MV",
"ML",
"MT",
"MH",
"MQ",
"MR",
"MU",
"MX",
"FM",
"MD",
"MN",
"ME",
"MA",
"MZ",
"MM",
"NA",
"NP",
"NL",
"NC",
"NZ",
"NI",
"NE",
"NG",
"NU",
"NF",
"MP",
"NO",
"OM",
"PK",
"PW",
"PA",
"PY",
"PE",
"PH",
"PL",
"PT",
"PR",
"QA",
"RO",
"RU",
"RW",
"KN",
"LC",
"WS",
"ST",
"SA",
"SN",
"RS",
"SC",
"SL",
"SG",
"SX",
"SK",
"SI",
"SO",
"ZA",
"SS",
"ES",
"LK",
"SD",
"SE",
"CH",
"SY",
"TJ",
"TZ",
"TH",
"TG",
"TO",
"TT",
"TN",
"TR",
"TM",
"TC",
"UG",
"UA",
"AE",
"GB",
"US",
"UY",
"UZ",
"VU",
"VE",
"VN",
"VI",
"YE",
"ZM",
"ZW"]



flight = {}


dests.each do |dest|
puts "scrape #{dest}"

begin

html = ScraperWiki.scrape("http://www.staralliance.com/destination_overview1.do?language=en&method=fetchAirports&country=#{dest}")

doc = Nokogiri::HTML(html)

row = doc.xpath("//table[@class='avadaytable']/tbody/tr")[0]

rescue

 puts "Something wrong"

end

unless row == nil
price = row.xpath("td[9]/div/label")
dep = row.xpath("td[1]/div")

time = Time.new

puts time.inspect
puts dep.inner_html
puts price.inner_html

flight = {}
flight['time'] = time.inspect
flight['from'] = departure
flight['dest'] = dest


ScraperWiki.save(["time"], flight)

sleep 2



end
end
end
end
