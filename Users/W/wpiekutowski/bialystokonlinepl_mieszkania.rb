require 'nokogiri'

url = "http://www.bialystokonline.pl/ogloszenia.php?catid=5"
html = ScraperWiki::scrape(url)
html.force_encoding('iso-8859-2')
doc = Nokogiri::HTML(html)
title_span_xpath = %Q|span[@style="font-size: 14px; font-weight: bold; color:black;"]|

doc.search(%Q|//td[@bgcolor="#FFFFCC"]|).each do |advert|
  p advert.to_html
  a = advert.search('a').first
  p a.to_html if a
  #p advert.at("#{title_span_xpath}").to_html

  #if cells.count == 12
  #  data = {
  #    country: cells[0].inner_html,
  #    years_in_school: cells[4].inner_html.to_i
  #  }
  #  ScraperWiki::save_sqlite(['country'], data) 
  #end
end
require 'nokogiri'

url = "http://www.bialystokonline.pl/ogloszenia.php?catid=5"
html = ScraperWiki::scrape(url)
html.force_encoding('iso-8859-2')
doc = Nokogiri::HTML(html)
title_span_xpath = %Q|span[@style="font-size: 14px; font-weight: bold; color:black;"]|

doc.search(%Q|//td[@bgcolor="#FFFFCC"]|).each do |advert|
  p advert.to_html
  a = advert.search('a').first
  p a.to_html if a
  #p advert.at("#{title_span_xpath}").to_html

  #if cells.count == 12
  #  data = {
  #    country: cells[0].inner_html,
  #    years_in_school: cells[4].inner_html.to_i
  #  }
  #  ScraperWiki::save_sqlite(['country'], data) 
  #end
end
