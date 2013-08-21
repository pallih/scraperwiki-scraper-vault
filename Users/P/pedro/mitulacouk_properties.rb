# encoding: utf-8

# Mitula property premium ads dataminer

require 'open-uri'
require 'nokogiri'

queries=[
"Sale/London",
"Sale/Birmingham",
"Sale/Leeds",
"Sale/Glasgow",
"Sale/Sheffield",
"Sale/Bradford",
"Sale/Edinburgh",
"Sale/Liverpool",
"Sale/Manchester",
"Sale/Bristol",
"Sale/Wakefield",
"Sale/Cardiff",
"Sale/Coventry",
"Sale/Nottingham",
"Sale/Leicester",
"Sale/Sunderland",
"Sale/Belfast",
"Sale/Newcastle upon Tyne",
"Sale/Brighton",
"Sale/Hull",
"Sale/Plymouth",
"Sale/Stoke-on-Trent",
"Sale/Wolverhampton",
"Sale/Derby",
"Sale/Swansea",
"Sale/Southampton",
"Sale/Salford",
"Sale/Aberdeen",
"Sale/Westminster",
"Sale/Portsmouth",
"Sale/York",
"Sale/Peterborough",
"Sale/Dundee",
"Sale/Lancaster",
"Sale/Oxford",
"Sale/Newport",
"Sale/Preston",
"Sale/St Albans",
"Sale/Norwich",
"Sale/Chester",
"Sale/Cambridge",
"Sale/Salisbury",
"Sale/Exeter",
"Sale/Gloucester",
"Sale/Lisburn",
"Sale/Chichester",
"Sale/Winchester",
"Sale/Londonderry",
"Sale/Carlisle",
"Sale/Worcester",
"Sale/Bath",
"Sale/Durham",
"Sale/Lincoln",
"Sale/Hereford",
"Sale/Armagh",
"Sale/Inverness",
"Sale/Stirling",
"Sale/Canterbury",
"Sale/Lichfield",
"Sale/Newry",
"Sale/Ripon",
"Sale/Bangor",
"Sale/Truro",
"Sale/Ely",
"Sale/Wells",
"Sale/St Davids",
"Rent/London",
"Rent/Birmingham",
"Rent/Leeds",
"Rent/Glasgow",
"Rent/Sheffield",
"Rent/Bradford",
"Rent/Edinburgh",
"Rent/Liverpool",
"Rent/Manchester",
"Rent/Bristol",
"Rent/Wakefield",
"Rent/Cardiff",
"Rent/Coventry",
"Rent/Nottingham",
"Rent/Leicester",
"Rent/Sunderland",
"Rent/Belfast",
"Rent/Newcastle upon Tyne",
"Rent/Brighton",
"Rent/Hull",
"Rent/Plymouth",
"Rent/Stoke-on-Trent",
"Rent/Wolverhampton",
"Rent/Derby",
"Rent/Swansea",
"Rent/Southampton",
"Rent/Salford",
"Rent/Aberdeen",
"Rent/Westminster",
"Rent/Portsmouth",
"Rent/York",
"Rent/Peterborough",
"Rent/Dundee",
"Rent/Lancaster",
"Rent/Oxford",
"Rent/Newport",
"Rent/Preston",
"Rent/St Albans",
"Rent/Norwich",
"Rent/Chester",
"Rent/Cambridge",
"Rent/Salisbury",
"Rent/Exeter",
"Rent/Gloucester",
"Rent/Lisburn",
"Rent/Chichester",
"Rent/Winchester",
"Rent/Londonderry",
"Rent/Carlisle",
"Rent/Worcester",
"Rent/Bath",
"Rent/Durham",
"Rent/Lincoln",
"Rent/Hereford",
"Rent/Armagh",
"Rent/Inverness",
"Rent/Stirling",
"Rent/Canterbury",
"Rent/Lichfield",
"Rent/Newry",
"Rent/Ripon",
"Rent/Bangor",
"Rent/Truro",
"Rent/Ely",
"Rent/Wells",
"Rent/St Davids"
]
counts = Hash.new(0)
j=0
while j<queries.count
  queryurl='http://property.mitula.co.uk/property/'+queries[j]
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

