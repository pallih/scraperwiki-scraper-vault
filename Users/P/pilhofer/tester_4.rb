# Blank Ruby

require 'rubygems'
require 'mechanize'

#puts "hello"

a = Mechanize.new
page = a.get("http://www.mshp.dps.mo.gov/HP71/SearchAction")

page.search('//table[@class="accidentOutput"]//tr').each do |node|
  #puts node.text
  #puts node.inner_html
  puts node.search('td')[1].text rescue nil
  
end