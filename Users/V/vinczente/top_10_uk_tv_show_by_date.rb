# Blank Ruby

# Blank Ruby
require 'json'
require 'date'
require 'digest/md5'
limits = [5, 10]
domain = 'http://www.seetonight.com'
now = Time.now
date_now = Time.utc(now.year,now.month,now.day)
i =1
limits.each do |limit|
 url = "http://www.seetonight.com/topic/_search.php?type=TV&order=TrendingNow&limit="+limit.to_s
 data = ScraperWiki.scrape(url)
 result = JSON.parse(data)

 result['items'].each do |item|
 record = {
  'id'=> item['topic_id'],
  'name'=> item['topic_name'],
  'picture'=> domain+item['topic_picture'],
  'position' => i,
  'popularity'=> item['topic_popularity'],
  'score'=> item['topic_score'],
  'url' => domain+item['topic_url'],
  'date' => date_now.strftime('%Y-%m-%d'),
  'key' => Digest::MD5.hexdigest(date_now.strftime('%Y-%m-%d')+'_'+item['topic_id'])
 }
 i = i+1
 ScraperWiki.save_sqlite(['key'], record)
 end
end