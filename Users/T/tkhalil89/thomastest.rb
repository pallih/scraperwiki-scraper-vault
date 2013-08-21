# Blank Ruby

p "Hello, coding in the cloud!"
html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
p html

require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr").each do |v|
  cells = v.search 'td'
  if cells.count == 12
    data = {
      country: cells[0].inner_html,
      years_in_school: cells[4].inner_html.to_i
    }
    ScraperWiki::save_sqlite(['country'], data)
  end
end

puts "This is a <em>fragment</em> of HTML."
ScraperWiki::attach("school_life_expectancy_in_years")
data = ScraperWiki::select(
    "* from school_life_expectancy_in_years.swdata 
    order by years_in_school desc limit 10"
)
puts data

puts "<table>"
puts "<tr><th>Country</th><th>Years in school</th>"
for d in data
  puts "<tr>"
  puts "<td>", d["country"], "</td>"
  puts "<td>", d["years_in_school"].to_s, "</td>"
  puts "</tr>"
end
puts "</table>"




