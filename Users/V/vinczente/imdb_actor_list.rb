require 'mechanize'
require 'digest/md5'

agent = Mechanize.new
show_id = 'tt0460649'
url = 'http://www.imdb.com/title/'+ show_id + '/'

agent.user_agent_alias = 'Mac Safari'

page = agent.get(url)
page.at("table.cast_list").search('tr')[1..-1].each do |r|
  record = {}
  if (r.search('a')[2]!=nil)
    record = {
       'actor_id' => r.search('a')[1].attribute('href').to_s.gsub('/name/', '').gsub('/',''),
       'show_id' => show_id,
       'actor_name' => r.search('a')[1].inner_text,
       'role' => r.search('a')[2].inner_text
     }
  else
    record = {
       'actor_id' => r.search('a')[1].attribute('href').to_s.gsub('/name/', '').gsub('/',''),
       'show_id' => show_id,
       'actor_name' => r.search('a')[1].inner_text,
       'role' => r.search('div')[0].inner_text.split("(")[0].strip
     }
  end
  ScraperWiki.save_sqlite(['actor_id'], record)
end
