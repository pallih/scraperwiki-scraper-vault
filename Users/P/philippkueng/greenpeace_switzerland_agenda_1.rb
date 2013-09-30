# Blank Ruby

puts "Extracting Greenpeace Switzerland Events from their Agenda"

html = ScraperWiki.scrape("http://www.greenpeace.org/switzerland/de/Aktiv-werden/Agenda/")

months = Hash.new
months["Januar"] = 1
months["Februar"] = 2
months["M&#132;rz"] = 3
months["April"] = 4
months["Mai"] = 5
months["Juni"] = 6
months["Juli"] = 7
months["August"] = 8
months["September"] = 9
months["Oktober"] = 10
months["November"] = 11
months["Dezember"] = 12

require 'nokogiri'

doc = Nokogiri::HTML(html)

counter = 1
timeout = 10 # so many empty but not nil elements are allowed until the scraping stops.

no_more_elements = false
while !no_more_elements

  # fetch the title, date and description
  heading = doc.search("h3#a#{counter}").first
  puts heading.inspect # output to the console
  if heading != nil
    gp_regex = /(\d{1,2})\.\s([\w|\&|\d|\;|\#]+)\s(\d{4})/
    #puts heading.inner_html.encode('utf-8')
    puts heading.inner_html.scan(gp_regex)
    scanned = heading.inner_html.scan(gp_regex)
    
    data = {'start_date' => "#{scanned[0][0]}/#{months[scanned[0][1]]}/#{scanned[0][2]}", 'title' => scanned[0]}
    ScraperWiki.save_sqlite(unique_keys=['title'], data=data)
  else
    if timeout == 0
      no_more_elements = true
    else
      timeout -= 1
    end
  end
  counter += 1
end# Blank Ruby

puts "Extracting Greenpeace Switzerland Events from their Agenda"

html = ScraperWiki.scrape("http://www.greenpeace.org/switzerland/de/Aktiv-werden/Agenda/")

months = Hash.new
months["Januar"] = 1
months["Februar"] = 2
months["M&#132;rz"] = 3
months["April"] = 4
months["Mai"] = 5
months["Juni"] = 6
months["Juli"] = 7
months["August"] = 8
months["September"] = 9
months["Oktober"] = 10
months["November"] = 11
months["Dezember"] = 12

require 'nokogiri'

doc = Nokogiri::HTML(html)

counter = 1
timeout = 10 # so many empty but not nil elements are allowed until the scraping stops.

no_more_elements = false
while !no_more_elements

  # fetch the title, date and description
  heading = doc.search("h3#a#{counter}").first
  puts heading.inspect # output to the console
  if heading != nil
    gp_regex = /(\d{1,2})\.\s([\w|\&|\d|\;|\#]+)\s(\d{4})/
    #puts heading.inner_html.encode('utf-8')
    puts heading.inner_html.scan(gp_regex)
    scanned = heading.inner_html.scan(gp_regex)
    
    data = {'start_date' => "#{scanned[0][0]}/#{months[scanned[0][1]]}/#{scanned[0][2]}", 'title' => scanned[0]}
    ScraperWiki.save_sqlite(unique_keys=['title'], data=data)
  else
    if timeout == 0
      no_more_elements = true
    else
      timeout -= 1
    end
  end
  counter += 1
end