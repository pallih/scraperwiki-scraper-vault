require 'rss/maker'

# データを取り出し
ScraperWiki.attach('japan_national_policy_unit_scraping')
datas = ScraperWiki.select("* from japan_national_policy_unit_scraping order by id asc")

# RSS を構築
rss = RSS::Maker.make("2.0") do |m|
  m.channel.title = '内閣官房　国家戦略室'
  m.channel.link = 'http://www.npu.go.jp/'

  for data in datas do
    item = m.items.new_item
    item.title = data['subject']
    item.link = data['uri']
    item.date = Time.parse(data['date'])
  end
end

# デフォルトは text/html で、広告用(?)の div が付加されてしまうので...
ScraperWiki.httpresponseheader( "Content-Type", "text/xml; charset=utf-8" )

# 出力
puts rss.to_s
