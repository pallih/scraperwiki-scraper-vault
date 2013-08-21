# Blank Ruby

puts "Scraping cantons of Switzerland with code and the according translations into different languages"

html = ScraperWiki.scrape("http://en.wikipedia.org/wiki/Cantons_of_Switzerland")

require 'nokogiri'

doc = Nokogiri::HTML(html)

for title in doc.search("div#bodyContent div.mw-content-ltr h2 span#Names_in_national_languages")
  #print(title)
end

#for v in doc.search("table.list tbody tr")
#  if v != nil
#    cells = v.search("td.tdusername a")
#    username = cells[0].inner_html[/([a-zA-Z0-9\s]+\s\()([\S]+)(\))/,2]
#    if username != nil
#      data = {'username' => username}
#    end
#    ScraperWiki.save_sqlite(unique_keys=['username'], data=data)
#  end
#end