# Blank Ruby
#require 'mechanize'
#require 'net/http'
require 'open-uri'
#require 'csv'
#require 'highline/import'
require 'scraperwiki'
require 'nokogiri'
#ag = Mechanize.new




# html = ScraperWiki.scrape("http://www.alehunt.com/venue/")
# puts html
#html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/education.htm")
# html = ScraperWiki.scrape("http://unstats.un.org/unsd/demographic/products/socind/default.htm")
#puts html
html = open("http://www.alehunt.com/venue/")
doc = Nokogiri::HTML(html)

## doc = Nokogiri::HTML(open('http://www.alehunt.com/venue/'))
#for v in doc.search("table[@id='venue-table']")
#  cells = v.search('td')
#  data = {
#    'name' => cells[0].inner_html,
#    'city' => cells[1].inner_html,
#    'country' => cells[2].inner_html,
#    'nr_of_beers' => cells[3].inner_html.to_i
#  }
#    puts data
#  # ScraperWiki.save_sqlite(unique_keys=['name'], data=data)
#  ScraperWiki.save_sqlite([], data=data)
#end

tables = doc.search("table[@id='venue-table']")
table = tables[0]
trs = table.search('tr')
trs.shift
for tr in trs
  cells = tr.search('td')
  data = {
    'name' => cells[0].inner_html,
    'city' => cells[1].inner_html,
    'country' => cells[2].inner_html,
    'nr_of_beers' => cells[3].inner_html.to_i
  }

#puts data
ScraperWiki.save_sqlite([], data=data)
end



# # baseurl = "http://www.alehunt.com/venue/"
# page = ag.get(baseurl)
# listing = page.parser.xpath("//table")
# trs = listing[0].xpath("//tr")
# trs.each do |tr|
#   tds = tr.search('td')
#   if tds[0].text == ''
#   else
#     link = tds[1].search('a')
#     link = "/venue/" + link.xpath("@href").to_s
#     ScraperWiki.save_sqlite(unique_keys=['App No', 'Title', 'Link'], data={"App No" => tds[1].text, "Title" => tds[2].text, "Link" => link} , table_name="PTOApps")
#   end
# end

#rc_code = page.parser.xpath("//input[@id='recaptcha_response_field']")







