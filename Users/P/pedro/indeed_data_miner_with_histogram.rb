# Blank Ruby

require 'open-uri'
require 'nokogiri'
queries=[
'Accountants',
'Actors',
'Actuaries',
'Acupuncturists',
'Acute+Care+Nurses',
'Nursing+in+Liverpool',
'Nursing+in+London']
counts = Hash.new(0)
array = Array.new(0)
j=0
#puts queries[0]
while j<queries.count
queryurl="http://www.indeed.co.uk/jobs?q="+queries[j]+"&l="
#puts queryurl
  doc = Nokogiri::HTML(open(queryurl))
  doc.search("span[@class = 'sdn']").each do |node|
  cells = node.search 'b'
    if cells.count > 0
    name=cells[0].inner_html
      data={
        advertiser: name,
        occurrences: counts[name] += 1
      }
      ScraperWiki::save_sqlite(['advertiser'], data)
     #Print to screen     
     #puts cells.text
     #array.push cells.text
    end
  end
j=j+1
end
#array.each { |name| counts[name] += 1 }
#Print histogram
#p counts