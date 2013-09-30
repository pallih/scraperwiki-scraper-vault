# Bomlo Nytt


require 'nokogiri'
html = ScraperWiki::scrape("ftp://kraftpriser.kt.no/Fastpris_Ukentlig/2010_25.txt")
#html = ScraperWiki::scrape("http://www.nbim.no/en/Investments/Return-on-the-fund/Fixed-income-management/")
#html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
p html

doc = Nokogiri::HTML(html)


doc.search("div#MainBody tr").each do |v|
#  cells = v.search 'td'
#  data = {
#    description: cells[0].inner_html,
#    stuff: cells[1].inner_html
#  }
#  ScraperWiki::save_sqlite(['description'], data)
#end

#doc.search("div#MainBody tr").each do |v|
#  cells = v.search 'td'
#  data = {
#    description: cells[0].inner_html,
#    stuff: cells[1].inner_html
#  }
#  ScraperWiki::save_sqlite(['description'], data)
#end


#doc.search("div[@align='left'] tr.tcont").each do |v|
#  cells = v.search 'td'
#  data = {
#    country: cells[0].inner_html,
#    men: cells[7].inner_html.to_i,
#    women: cells[10].inner_html.to_i
#  }
#  ScraperWiki::save_sqlite(['country'], data)
#end
# Bomlo Nytt


require 'nokogiri'
html = ScraperWiki::scrape("ftp://kraftpriser.kt.no/Fastpris_Ukentlig/2010_25.txt")
#html = ScraperWiki::scrape("http://www.nbim.no/en/Investments/Return-on-the-fund/Fixed-income-management/")
#html = ScraperWiki::scrape("http://web.archive.org/web/20110514112442/http://unstats.un.org/unsd/demographic/products/socind/education.htm")
p html

doc = Nokogiri::HTML(html)


doc.search("div#MainBody tr").each do |v|
#  cells = v.search 'td'
#  data = {
#    description: cells[0].inner_html,
#    stuff: cells[1].inner_html
#  }
#  ScraperWiki::save_sqlite(['description'], data)
#end

#doc.search("div#MainBody tr").each do |v|
#  cells = v.search 'td'
#  data = {
#    description: cells[0].inner_html,
#    stuff: cells[1].inner_html
#  }
#  ScraperWiki::save_sqlite(['description'], data)
#end


#doc.search("div[@align='left'] tr.tcont").each do |v|
#  cells = v.search 'td'
#  data = {
#    country: cells[0].inner_html,
#    men: cells[7].inner_html.to_i,
#    women: cells[10].inner_html.to_i
#  }
#  ScraperWiki::save_sqlite(['country'], data)
#end
