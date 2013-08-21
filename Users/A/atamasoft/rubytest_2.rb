require 'nokogiri'
require 'open-uri'
require 'kconv'

# @see http://d.hatena.ne.jp/Mariyudu/20110903/1315037137

#charset 宣言無しなので注意
TopUri = "http://www.shitamachi.net/wa/jazz/index.htm" 

# 最新記事のタイトル等を取得
dom = Nokogiri::HTML(open(TopUri))
title = dom.xpath('//td/p/font[@color="#ff3300"]/b')[0].text
posted = dom.xpath('//td/div/p//font[@color="#000000"]')[0].text + ' 00:00:00 +0900'

# 結果を保存
result = []
result << {
  'id' => 1,
/*
  'c_title' => cTitle,
  'c_link' => TopUri,
  'c_desc' => cDesc,
  'title' => title,
  'link' => latestArticleUri,
  'date' => Time.parse(posted).to_s
*/
}
ScraperWiki.save(['id'], result)

