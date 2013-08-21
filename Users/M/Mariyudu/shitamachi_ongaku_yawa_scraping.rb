# 「下町音楽夜話」の更新をチェックする
require 'nokogiri'
require 'open-uri'
require 'kconv'

TopUri = "http://www.shitamachi.net/wa/jazz/index.htm" #charset 宣言無しなので注意

# 最新記事の URL 等を取得
dom = Nokogiri::HTML(open(TopUri).read.toutf8)
frame = dom.xpath('//frame[@name="jazz"]')
latestArticleUri = "http://www.shitamachi.net/wa/jazz/" + frame[0]["src"]
cTitle = dom.xpath('//title')[0].text
cDesc = dom.xpath('//head/meta[@name="description"]')[0]["content"]

# 最新記事のタイトル等を取得
dom = Nokogiri::HTML(open(latestArticleUri))
title = dom.xpath('//td/p/font[@color="#ff3300"]/b')[0].text
posted = dom.xpath('//td/div/p//font[@color="#000000"]')[0].text + ' 00:00:00 +0900'

# 結果を保存
result = []
result << {
  'id' => 1,
  'c_title' => cTitle,
  'c_link' => TopUri,
  'c_desc' => cDesc,
  'title' => title,
  'link' => latestArticleUri,
  'date' => Time.parse(posted).to_s
}
ScraperWiki.save(['id'], result)

