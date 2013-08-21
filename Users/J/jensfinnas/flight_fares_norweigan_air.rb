require 'rubygems'  
 require 'nokogiri'  
 require 'open-uri' 
 require 'mechanize'

#FLIGHT DAY: 20.10.2011

dests = ["AAL",
"ACE",
"AES",
"AGA",
"AGP",
"ALC",
"ALCA",
"ALF",
"AMS",
"ARN",
"ATH",
"AYT",
"BCN",
"BDU",
"BEG",
"BGO",
"BLL",
"BOJ",
"BOO",
"BUD",
"CHQ",
"CPH",
"DBV",
"DUB",
"DUS",
"DXB",
"EDI",
"EVE",
"FAO",
"FCO",
"FNC",
"FRA",
"GDN",
"GNB",
"GOT",
"GVA",
"HAM",
"HAU",
"HEL",
"KKN",
"KRK",
"KRP",
"KRS",
"LCA",
"LED",
"LGW",
"LLA",
"LPA",
"MAN",
"MJV",
"MLA",
"MMX",
"MOL",
"MUC",
"MXP",
"NCE",
"OLB",
"ORY",
"OSL",
"OSLA",
"OUL",
"PLQ",
"PMI",
"PMO",
"POZ",
"PRG",
"PSA",
"PUY",
"RAK",
"RIX",
"RVN",
"RYG",
"SJJ",
"SPU",
"SVG",
"SXF",
"SZG",
"SZZ",
"TFS",
"TLL",
"TLV",
"TOS",
"TRD",
"TRF",
"UME",
"WAW",
"VCE",
"VIE",
"VNO",
"ZAG"]

departures = ["MMX","ARN", "GOT"]
days = ["26","27","28","29","30"]

flight = {}

departures.each do |departure|
dests.each do |dest|
days.each do |day|
puts "scrape #{departure} to #{dest} @ #{day} Oct"

begin

html = ScraperWiki.scrape("http://www.norwegian.com/se/flyg/valj-flyvning/?D_City=#{departure}&A_City=#{dest}&TripType=1&D_Day=30&D_Month=201109&D_SelectedDay=#{day}&R_Day=30&R_Month=201109&R_SelectedDay=30&AgreementCodeFK=-1&CurrencyCode=SEK&rnd=30615&processid=54422")

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
flight['dep'] = dep.inner_html
flight['price'] = price.inner_html
flight['day'] = day

ScraperWiki.save(["time"], flight)

sleep 2



end
end
end
end


