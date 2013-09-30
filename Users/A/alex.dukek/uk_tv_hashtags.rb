# Blank Ruby
require 'mechanize'

url = 'http://zeebox.com/tms/brands/1.json'
data = ScraperWiki.scrape(url)
result = JSON.parse(data)
all_hashtags = ''
result['twerms'].each do |twerm|
  all_hashtags += twerm['text'] + ','
end

record = {
  'id' => result['id'],
  'title' => result['title'],
  'hashtags' => all_hashtags.strip[0..-2],
  'image' => result['image']['url']
}
ScraperWiki.save_sqlite(['id'], record)# Blank Ruby
require 'mechanize'

url = 'http://zeebox.com/tms/brands/1.json'
data = ScraperWiki.scrape(url)
result = JSON.parse(data)
all_hashtags = ''
result['twerms'].each do |twerm|
  all_hashtags += twerm['text'] + ','
end

record = {
  'id' => result['id'],
  'title' => result['title'],
  'hashtags' => all_hashtags.strip[0..-2],
  'image' => result['image']['url']
}
ScraperWiki.save_sqlite(['id'], record)