# encoding: utf-8

# Mitula car premium ads dataminer

require 'open-uri'
require 'nokogiri'

queries=[
"Ford ",
"Chevrolet ",
"Mistubishi ",
"Toyota ",
"Honda ",
"Mercedes-Benz ",
"Lincoln ",
"Subaru ",
"Mazda ",
"Dodge ",
"Lamborghini ",
"McLaren ",
"Chrysler ",
"Pagani ",
"Austin ",
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
"Smart4two ",
"Shelby ",
"Desota ",
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
"Maruti ",
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
"Wells",
"St Davids"
]
counts = Hash.new(0)
j=0
while j<queries.count
  queryurl='http://cars.mitula.co.uk/cars/'+queries[j]
 # puts queryurl
  doc = Nokogiri::HTML(open(URI::encode(queryurl)))
doc.search("div[@class='listing sponsored']").each do |node|
  #puts node
    cells=node.search("small") 
 if node.count > 0
   # puts cells.text
    name=cells.text.gsub!(/.*?(?=in )/, "") 
   # puts name
    name.slice! "in "  
   # puts name
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

# Mitula car premium ads dataminer

require 'open-uri'
require 'nokogiri'

queries=[
"Ford ",
"Chevrolet ",
"Mistubishi ",
"Toyota ",
"Honda ",
"Mercedes-Benz ",
"Lincoln ",
"Subaru ",
"Mazda ",
"Dodge ",
"Lamborghini ",
"McLaren ",
"Chrysler ",
"Pagani ",
"Austin ",
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
"Smart4two ",
"Shelby ",
"Desota ",
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
"Maruti ",
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
"Wells",
"St Davids"
]
counts = Hash.new(0)
j=0
while j<queries.count
  queryurl='http://cars.mitula.co.uk/cars/'+queries[j]
 # puts queryurl
  doc = Nokogiri::HTML(open(URI::encode(queryurl)))
doc.search("div[@class='listing sponsored']").each do |node|
  #puts node
    cells=node.search("small") 
 if node.count > 0
   # puts cells.text
    name=cells.text.gsub!(/.*?(?=in )/, "") 
   # puts name
    name.slice! "in "  
   # puts name
    data={
         advertiser: name,
         occurrences: counts[name] += 1
    }
          ScraperWiki::save_sqlite(['advertiser'], data)
    end
  end
j=j+1
end

