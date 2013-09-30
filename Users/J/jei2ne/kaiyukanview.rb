# encoding: utf-8
require 'rss/maker'

sourcescraper = 'kaiyukan'
ScraperWiki.attach("kaiyukan")
data = ScraperWiki.select(
    "* from kaiyukan.swdata order by id asc"
)

# RSS を構築
rss = RSS::Maker.make("2.0") do |m|
  m.channel.title = "天保山マーケットプレイス パフォーマンススケジュール"
  m.channel.link = "http://www.kaiyukan.com/thv/marketplace/performance/index.html"
  m.channel.description = "天保山マーケットプレイスで行われているストリートパフォーマンスのスケジュールです。"
  m.channel.language = "ja"

  item = m.items.new_item
  item.title = Time.now.strftime("%Y年%m月%d日") + "時点"
  item.link = "http://www.kaiyukan.com/thv/marketplace/performance/index.html"
  item.date = Time.now
  desc = ""
  for d in data do
    desc.concat d["date"] + " " + d["performer"] + "<br />"
  end
  item.description = desc
end

# デフォルトは text/html で、広告用(?)の div が付加されてしまうので...
ScraperWiki.httpresponseheader( "Content-Type", "text/xml; charset=utf-8" )

# 出力
puts rss.to_s

# encoding: utf-8
require 'rss/maker'

sourcescraper = 'kaiyukan'
ScraperWiki.attach("kaiyukan")
data = ScraperWiki.select(
    "* from kaiyukan.swdata order by id asc"
)

# RSS を構築
rss = RSS::Maker.make("2.0") do |m|
  m.channel.title = "天保山マーケットプレイス パフォーマンススケジュール"
  m.channel.link = "http://www.kaiyukan.com/thv/marketplace/performance/index.html"
  m.channel.description = "天保山マーケットプレイスで行われているストリートパフォーマンスのスケジュールです。"
  m.channel.language = "ja"

  item = m.items.new_item
  item.title = Time.now.strftime("%Y年%m月%d日") + "時点"
  item.link = "http://www.kaiyukan.com/thv/marketplace/performance/index.html"
  item.date = Time.now
  desc = ""
  for d in data do
    desc.concat d["date"] + " " + d["performer"] + "<br />"
  end
  item.description = desc
end

# デフォルトは text/html で、広告用(?)の div が付加されてしまうので...
ScraperWiki.httpresponseheader( "Content-Type", "text/xml; charset=utf-8" )

# 出力
puts rss.to_s

