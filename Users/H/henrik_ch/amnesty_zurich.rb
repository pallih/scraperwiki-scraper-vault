# Blank Ruby

puts "Extracting events from Amnesty Zurich"

html = ScraperWiki.scrape("http://www.amnesty-zh.ch")

require 'nokogiri'

doc = Nokogiri::HTML(html)
puts doc
for v in doc.search("#content div")
  puts v.inspect
  if v != nil
    cells = v.search("h2 a")
    eventTitle = cells[0].inner_html
    if eventTitle != nil
      data = {'title' => eventTitle}
    end
    ScraperWiki.save_sqlite(unique_keys=['title'], data=data)
  end
end# Blank Ruby

puts "Extracting events from Amnesty Zurich"

html = ScraperWiki.scrape("http://www.amnesty-zh.ch")

require 'nokogiri'

doc = Nokogiri::HTML(html)
puts doc
for v in doc.search("#content div")
  puts v.inspect
  if v != nil
    cells = v.search("h2 a")
    eventTitle = cells[0].inner_html
    if eventTitle != nil
      data = {'title' => eventTitle}
    end
    ScraperWiki.save_sqlite(unique_keys=['title'], data=data)
  end
end