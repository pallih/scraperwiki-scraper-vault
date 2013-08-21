# Blank Ruby

puts "Extracting twitter usernames from twittercharts.ch"

html = ScraperWiki.scrape("http://twittercharts.ch")

require 'nokogiri'

doc = Nokogiri::HTML(html)
for v in doc.search("table.list tbody tr")
  if v != nil
    cells = v.search("td.tdusername a")
    username = cells[0].inner_html[/([a-zA-Z0-9\s]+\s\()([\S]+)(\))/,2]
    if username != nil
      data = {'username' => username}
    end
    ScraperWiki.save_sqlite(unique_keys=['username'], data=data)
  end
end