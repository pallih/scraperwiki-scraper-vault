# Blank Ruby

#http://hu.wikipedia.org/w/index.php?title=Technol%C3%B3giai_szingularit%C3%A1s&action=history

#url = "http://hu.wikipedia.org/w/index.php?title=Technol%C3%B3giai_szingularit%C3%A1s&action=history"
#url = "index.hu"
#url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"
#url = "http://hu.wikipedia.org/wiki/Technol%C3%B3giai_szingularit%C3%A1s"
url = "http://en.wikipedia.org/wiki/Technological_singularity"

html = ScraperWiki::scrape(url)           

p html

require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr").each do |v|
  cells = v.search 'td'
  if cells.count == 12
    data = {
      country: cells[0].inner_html,
      years_in_school: cells[4].inner_html.to_i
    }
    puts data.to_json
  end
end

#ScraperWiki::save_sqlite(['country'], data)# Blank Ruby

#http://hu.wikipedia.org/w/index.php?title=Technol%C3%B3giai_szingularit%C3%A1s&action=history

#url = "http://hu.wikipedia.org/w/index.php?title=Technol%C3%B3giai_szingularit%C3%A1s&action=history"
#url = "index.hu"
#url = "http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm"
#url = "http://hu.wikipedia.org/wiki/Technol%C3%B3giai_szingularit%C3%A1s"
url = "http://en.wikipedia.org/wiki/Technological_singularity"

html = ScraperWiki::scrape(url)           

p html

require 'nokogiri'
doc = Nokogiri::HTML html
doc.search("div[@align='left'] tr").each do |v|
  cells = v.search 'td'
  if cells.count == 12
    data = {
      country: cells[0].inner_html,
      years_in_school: cells[4].inner_html.to_i
    }
    puts data.to_json
  end
end

#ScraperWiki::save_sqlite(['country'], data)