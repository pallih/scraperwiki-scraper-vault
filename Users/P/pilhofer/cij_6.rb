# Blank Ruby

require "mechanize"

ua = Mechanize.new
page = ua.get('http://ire.aronpilhofer.com/scrape.html')
page.search('//table//tr').each do |row|
  row.search('td').each do |data|
    puts data.text
  end
end

# Blank Ruby

require "mechanize"

ua = Mechanize.new
page = ua.get('http://ire.aronpilhofer.com/scrape.html')
page.search('//table//tr').each do |row|
  row.search('td').each do |data|
    puts data.text
  end
end

