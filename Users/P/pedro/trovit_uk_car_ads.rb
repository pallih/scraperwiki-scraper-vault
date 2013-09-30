# encoding: utf-8

# Trovit.co.uk premium car ads dataminer

require 'open-uri'
require 'nokogiri'
queries=[
"Ford",
"Chevrolet",
"Mistubishi",
"Toyota",
"Honda",
"Mercedes-Benz",
"Lincoln",
"Subaru",
"Mazda",
"Dodge",
"Lamborghini",
"McLaren",
"Chrysler",
"Pagani",
"Austin",
"Aston Martin ",
"Alfa Romeo ",
"Holden ",
"Fiat ",
"Volks Wagen ",
"Suzuki ",
"Acura ",
"Audi ",
"BMW ",
"Bentley ",
"Bugatti ",
"Rolls Royce ",
"GMC ",
"Kia ",
"Hyundai ",
"Smart",
"Shelby ",
"Studebaker ",
"Plymouth ",
"Packard ",
"AMC ",
"Hummer ",
"Skoda ",
"Pierce Arrow ",
"Oldsmobile ",
"Pontiac ",
"Cadillac ",
"Buick ",
"Lexus ",
"Saturn ",
"Auburn ",
"Cord ",
"Henry J ",
"Lasalle ",
"Maserati ",
"Porsche ",
"Citroen ",
"Lotus ",
"Hennessey ",
"Renault ",
"Saleen ",
"Peugeot ",
"Alpina ",
"Ariel ",
"Perodua ",
"Tata ",
"Tesla",
"Nissan ",
"FPV",
"HSV",
"Lincoln",
"Mercury",
"London",
"Birmingham",
"Leeds",
"Glasgow",
"Sheffield",
"Bradford",
"Edinburgh",
"Liverpool",
"Manchester",
"Bristol",
"Wakefield",
"Cardiff",
"Coventry",
"Nottingham",
"Leicester",
"Sunderland",
"Belfast",
"Newcastle upon Tyne",
"Brighton",
"Hull",
"Plymouth",
"Stoke-on-Trent",
"Wolverhampton",
"Derby",
"Swansea",
"Southampton",
"Salford",
"Aberdeen",
"Westminster",
"Portsmouth",
"York",
"Peterborough",
"Dundee",
"Lancaster",
"Oxford",
"Newport",
"Preston",
"St Albans",
"Norwich",
"Chester",
"Cambridge",
"Salisbury",
"Exeter",
"Gloucester",
"Lisburn",
"Chichester",
"Winchester",
"Londonderry",
"Carlisle",
"Worcester",
"Bath",
"Durham",
"Lincoln",
"Hereford",
"Armagh",
"Inverness",
"Stirling",
"Canterbury",
"Lichfield",
"Newry",
"Ripon",
"Bangor",
"Truro",
"Ely",
"Wells"
]
counts = Hash.new(0)
j=0
while j<queries.count
  queryurl='http://cars.trovit.co.uk/index.php/cod.search_cars/what_d.'+queries[j]
 # puts queryurl
  doc = Nokogiri::HTML(open(URI::encode(queryurl)))
doc.search("div[@id='wrapper_ppc_top']").each do |node|
 innode=node.search("p[@class='description']")
    cells=innode.search("small")  
    if(cells.count>0)  
    #puts cells.text
    name=cells.text
    data={
         advertiser: name,
         occurrences: counts[name] += 1
    }
          ScraperWiki::save_sqlite(['advertiser'], data)
   end
end
doc.search("div[@id='wrapper_ppc_bottom']").each do |node|
 innode=node.search("p[@class='description']")
    cells=innode.search("small")   
   # puts cells.text
    if(cells.count>0)  
   name=cells.text
   data={
         advertiser: name,
         occurrences: counts[name] += 1
    }
          ScraperWiki::save_sqlite(['advertiser'], data)
  end
  end
j=j+1
end
# encoding: utf-8

# Trovit.co.uk premium car ads dataminer

require 'open-uri'
require 'nokogiri'
queries=[
"Ford",
"Chevrolet",
"Mistubishi",
"Toyota",
"Honda",
"Mercedes-Benz",
"Lincoln",
"Subaru",
"Mazda",
"Dodge",
"Lamborghini",
"McLaren",
"Chrysler",
"Pagani",
"Austin",
"Aston Martin ",
"Alfa Romeo ",
"Holden ",
"Fiat ",
"Volks Wagen ",
"Suzuki ",
"Acura ",
"Audi ",
"BMW ",
"Bentley ",
"Bugatti ",
"Rolls Royce ",
"GMC ",
"Kia ",
"Hyundai ",
"Smart",
"Shelby ",
"Studebaker ",
"Plymouth ",
"Packard ",
"AMC ",
"Hummer ",
"Skoda ",
"Pierce Arrow ",
"Oldsmobile ",
"Pontiac ",
"Cadillac ",
"Buick ",
"Lexus ",
"Saturn ",
"Auburn ",
"Cord ",
"Henry J ",
"Lasalle ",
"Maserati ",
"Porsche ",
"Citroen ",
"Lotus ",
"Hennessey ",
"Renault ",
"Saleen ",
"Peugeot ",
"Alpina ",
"Ariel ",
"Perodua ",
"Tata ",
"Tesla",
"Nissan ",
"FPV",
"HSV",
"Lincoln",
"Mercury",
"London",
"Birmingham",
"Leeds",
"Glasgow",
"Sheffield",
"Bradford",
"Edinburgh",
"Liverpool",
"Manchester",
"Bristol",
"Wakefield",
"Cardiff",
"Coventry",
"Nottingham",
"Leicester",
"Sunderland",
"Belfast",
"Newcastle upon Tyne",
"Brighton",
"Hull",
"Plymouth",
"Stoke-on-Trent",
"Wolverhampton",
"Derby",
"Swansea",
"Southampton",
"Salford",
"Aberdeen",
"Westminster",
"Portsmouth",
"York",
"Peterborough",
"Dundee",
"Lancaster",
"Oxford",
"Newport",
"Preston",
"St Albans",
"Norwich",
"Chester",
"Cambridge",
"Salisbury",
"Exeter",
"Gloucester",
"Lisburn",
"Chichester",
"Winchester",
"Londonderry",
"Carlisle",
"Worcester",
"Bath",
"Durham",
"Lincoln",
"Hereford",
"Armagh",
"Inverness",
"Stirling",
"Canterbury",
"Lichfield",
"Newry",
"Ripon",
"Bangor",
"Truro",
"Ely",
"Wells"
]
counts = Hash.new(0)
j=0
while j<queries.count
  queryurl='http://cars.trovit.co.uk/index.php/cod.search_cars/what_d.'+queries[j]
 # puts queryurl
  doc = Nokogiri::HTML(open(URI::encode(queryurl)))
doc.search("div[@id='wrapper_ppc_top']").each do |node|
 innode=node.search("p[@class='description']")
    cells=innode.search("small")  
    if(cells.count>0)  
    #puts cells.text
    name=cells.text
    data={
         advertiser: name,
         occurrences: counts[name] += 1
    }
          ScraperWiki::save_sqlite(['advertiser'], data)
   end
end
doc.search("div[@id='wrapper_ppc_bottom']").each do |node|
 innode=node.search("p[@class='description']")
    cells=innode.search("small")   
   # puts cells.text
    if(cells.count>0)  
   name=cells.text
   data={
         advertiser: name,
         occurrences: counts[name] += 1
    }
          ScraperWiki::save_sqlite(['advertiser'], data)
  end
  end
j=j+1
end
