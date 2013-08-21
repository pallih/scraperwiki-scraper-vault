require 'nokogiri'
#require 'time'
#require 'date'

agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.54.16 (KHTML, like Gecko) Version/5.1.4 Safari/534.54.16"

html = ScraperWiki.scrape("http://en.wikipedia.org/wiki/List_of_Prime_Ministers_of_the_United_Kingdom")


html.force_encoding("UTF-8")
doc = Nokogiri::HTML(html)

name = ""
party = ""
prev_name = ""
from = ""
to = ""
continuation = false


tables = doc.xpath("//table[@class='wikitable']")

#skip the first one, it's in a different format to the others
tables[1..tables.size].each do |table|
  rows = table.xpath("tr")
  #skip the first row - it's a header
  counter = 0 #set the counter so it knows it's supposed to be an int
  rows[1..rows.size].each do |row|
    cells = row.xpath("td")
    #take a look at the first cell
    # if it's empty with a background color set, it's the start of something
    counter = 1 if cells[0].text == "" and cells[0].xpath("@style").to_s.include?("background-color")
    case counter
    when 1  
      name = cells[2].xpath("a").text
      #if the name looks blank, it's probably hiding in a bold tag
      name = cells[2].xpath("b/a").text if name == ""
      #if it's still blank, it's a continuation
      if name == ""
        name = prev_name 
        continuation = true
      else
        prev_name = name
      end
      if continuation
        party = cells[4].text
        from = cells[1].text.gsub("\n", " ")
        to = cells[2].text.gsub("\n", " ").gsub("\u2020", "")
      else
        party = cells[6].text
        from = cells[3].text.gsub("\n", " ")
        to = cells[4].text.gsub("\n", " ").gsub("\u2020", "")
      end
    else
      if cells.size == 3
        to = cells[1].text.gsub("\n", " ").gsub("\u2020", "")
      elsif cells.size == 1 and cells[0].xpath("@colspan").to_s == "5"
        notes = cells[0].xpath("small").text
  
        #debug
        p "name: #{name}"
        p "party: #{party}"
        p "from: #{from}"
        p "to: #{to}"
        p "notes: #{notes}"
        p " --- "

        record = {'name' => name, 'party' => party, 'pm_from' => from, 'pm_to' => to, 'notes' => notes}
        ScraperWiki.save(['name', 'pm_from'], record)
        continuation = false
      end
    end
    counter += 1
  end
end