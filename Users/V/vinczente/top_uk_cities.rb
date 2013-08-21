# Blank Ruby
require 'mechanize'

url = 'http://en.wikipedia.org/wiki/List_of_largest_United_Kingdom_settlements_by_population'

agent = Mechanize.new
agent.user_agent_alias = 'Linux Mozilla'
page = agent.get(url)

def remove_tags(html_stuff)
return html_stuff.inner_html.gsub(/<\/?[^>]*>/, "")
end


page.at("table.wikitable").search('tr')[1..-1].each do |r|
position = remove_tags(r.search('td')[0])
name = remove_tags(r.search('td')[1])
population = remove_tags(r.search('td')[2])
country = remove_tags(r.search('td')[3])
county = remove_tags(r.search('td')[4])
notes = remove_tags(r.search('td')[5])
record = {
   'position' => position,
   'name' => name,
   'population' => population,
   'country' => country,
   'county' => county,
   'notes' => notes
 }
 ScraperWiki.save_sqlite(['position'], record)
end