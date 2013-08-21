html = ScraperWiki::scrape("http://tv.ekolay.net/kanal/8/Star.aspx")           
p html

require 'nokogiri'           
doc = Nokogiri::HTML html

=begin
doc.search(".wd70").each do |v|
  cells = v.search 'td'
  if cells.count == 12
    data = {
      country: cells[0].inner_html,
      years_in_school: cells[4].inner_html.to_i
    }
    puts data.to_json
  end
=end

doc.css("td a").each do |link|           
  puts link.inner html
end

#.wd70 , .wd274
# //*[contains(concat( " ", @class, " " ), concat( " ", "wd70", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "wd274", " " ))]