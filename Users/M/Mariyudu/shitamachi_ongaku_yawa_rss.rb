require 'rss/maker'

# データを取り出し
ScraperWiki.attach("shitamachi_ongaku_yawa_scraping")
datas = ScraperWiki.select("* from shitamachi_ongaku_yawa_scraping.swdata order by id asc")

# RSS を構築
rss = RSS::Maker.make("2.0") do |m|
  m.channel.title = datas[0]['c_title']
  m.channel.link = datas[0]['c_link']
  m.channel.description = datas[0]['c_desc']

  for data in datas do
    item = m.items.new_item
    item.title = data['title']
    item.link = data['link']
    item.date = Time.parse(data['date'])
  end
end

# デフォルトは text/html で、広告用(?)の div が付加されてしまうので...
ScraperWiki.httpresponseheader( "Content-Type", "text/xml; charset=utf-8" )

# 出力
puts rss.to_s
