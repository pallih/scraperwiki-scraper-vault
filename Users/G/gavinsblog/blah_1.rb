require "mechanize"

ua = Mechanize.new
page = ua.get("http://www.kildarestreet.com/debates/?id=2012-07-10.891.0&s=tabular+form#g892.0")
page.search("//table//tr").each do |row| 
  row.search("td").each do |data|
    puts data.text
  end
end

