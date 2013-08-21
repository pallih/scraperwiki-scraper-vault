require 'mechanize'

ua = Mechanize.new
page = ua.get("http://ire.aronpilhofer.com/scrape.html")

results = []
page.search('//table//tr').each do |row|
  results << row.search('td').map {|n| n.text }
end
puts results