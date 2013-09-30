require 'nokogiri'
require 'open-uri'

isbn = 9780205763122


url = "http://www.ecampus.com\/bk_detail14.asp?isbn=" + isbn.to_s
doc = Nokogiri::HTML open(url)
doc.search( "//div[@class='rental-row']" ).each do |rental|
  term= rental.search("div[@id^='term']").inner_html.to_s.strip
  duedate = rental.search("div[@id^='due']").inner_html.to_s.strip
  price = rental.search("div[@id^='price']").inner_html.to_s.strip
  puts term + "|" + duedate + "|" + price
end
doc.search( "//div[@class='prices']/label/div[@class='row']" ).each do |book|
  condition= book.search("div[@class^='type']").inner_html.to_s.strip
  price = book.search("div[@class^='price']").inner_html.to_s.strip
  puts condition + "|" + price
endrequire 'nokogiri'
require 'open-uri'

isbn = 9780205763122


url = "http://www.ecampus.com\/bk_detail14.asp?isbn=" + isbn.to_s
doc = Nokogiri::HTML open(url)
doc.search( "//div[@class='rental-row']" ).each do |rental|
  term= rental.search("div[@id^='term']").inner_html.to_s.strip
  duedate = rental.search("div[@id^='due']").inner_html.to_s.strip
  price = rental.search("div[@id^='price']").inner_html.to_s.strip
  puts term + "|" + duedate + "|" + price
end
doc.search( "//div[@class='prices']/label/div[@class='row']" ).each do |book|
  condition= book.search("div[@class^='type']").inner_html.to_s.strip
  price = book.search("div[@class^='price']").inner_html.to_s.strip
  puts condition + "|" + price
end