# Blank Ruby
require 'mechanize'
require 'digest/md5'

agent = Mechanize.new
url = 'http://www.extrafootie.co.uk/clubs/'

page = agent.get(url)
page.at("table").search('tr')[1..-1].each do |r|
    record = {
       'id' => r.search('td')[1].search('img').attribute('src').to_s.gsub('http://www.extrafootie.co.uk/resources/team_images/','').gsub('_small.gif', ''),
       'name' =>  r.search('td.tableUser')[0].inner_text
     }
ScraperWiki.save_sqlite(['id'], record)
end