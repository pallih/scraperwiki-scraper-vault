#http://www.cuantocabron.com/top/todos/p/1

html = ScraperWiki::scrape("http://www.cuantocabron.com/top/todos/p/1")           

require 'nokogiri'           

doc = Nokogiri::HTML html
doc.search("p[@class = 'story_content']").each do |v|
  puts v
#  t = v.search 'h2'
#  f = v.search 'div.'
#  data = {
#    title: t[0].inner_html,
#    years_in_school: cells[4].inner_html
#  }
#  puts data.to_json
end
