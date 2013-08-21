# coding: utf-8

require 'rss/maker'

# データを取り出し
ScraperWiki.attach("abenatsumi_blog")
datas = ScraperWiki.select("* from swdata")

# RSS を構築
rss = RSS::Maker.make("2.0") do |m|
  m.channel.title = "安倍なつみ blog"
  m.channel.link = "http://www.abe-natsumi.com/blog/"
  m.channel.description = "scraped via https://scraperwiki.com/scrapers/abenatsumi_blog/"

  for data in datas do
    item = m.items.new_item
    item.title = data['title']
    item.link = data['link']
    item.date = Time.parse(data['date'])
    item.description = data['content']
  end
end

# デフォルトは text/html で、広告用(?)の div が付加されてしまうので...
ScraperWiki.httpresponseheader( "Content-Type", "text/xml; charset=utf-8" )

# 出力
puts rss.to_s
