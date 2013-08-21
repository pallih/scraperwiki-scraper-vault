# Blank Ruby

puts "Extracting tyhafan Events from their Agenda"

html = ScraperWiki.scrape("http://www.tyhafan.org/our-events/")

months = Hash.new
months["January"] = 1
months["February"] = 2
months["March"] = 3
months["April"] = 4
months["May"] = 5
months["June"] = 6
months["July"] = 7
months["August"] = 8
months["September"] = 9
months["October"] = 10
months["November"] = 11
months["December"] = 12

require 'nokogiri'

puts html

doc = Nokogiri::HTML(html)

puts doc

counter = 0
for v in doc.search("div.wysiwyg")
  puts v.inspect
  if v != nil and counter != 0
    cells = v.search("td")

    puts cells[0]

    #if username != nil
    #  data = {'username' => username}
    #end
    #ScraperWiki.save_sqlite(unique_keys=['username'], data=data)
  end
  counter += 1
end