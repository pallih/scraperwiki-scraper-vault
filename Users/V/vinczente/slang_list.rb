# Blank Ruby
require 'mechanize'
require 'digest/md5'

url = 'http://www.internetslang.com/all.asp'

agent = Mechanize.new
agent.user_agent_alias = 'Mac Safari'
page = agent.get(url)

page.at("table").search('tr')[68..-1].each do |r|
  if(r.search('td')[0]!=nil)
    record = {
       'slang' => r.search('td')[0].inner_html.gsub(/<\/?[^>]*>/, ""),
       'equivalent' => r.search('td')[1].inner_html,
       'key' => Digest::MD5.hexdigest(r.search('td')[0].inner_html + '-' + r.search('td')[1].inner_html)
    }
    ScraperWiki.save_sqlite(['key'], record)
  end
end