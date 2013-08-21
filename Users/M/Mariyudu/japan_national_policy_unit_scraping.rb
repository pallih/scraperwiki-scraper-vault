# 「国家戦略室」の更新をチェックする
require 'nokogiri'
require 'open-uri'
require 'kconv'

TopUri = "http://www.npu.go.jp/"

# 最新記事の URL 等を取得
datas = []
id = 1
dom = Nokogiri::HTML(open(TopUri).read.toutf8)
dom.css('div#tabs-1 ul.latestinfo li').each do |li|
  spans = li.xpath('span')
  datas << {
    'id' => id,
    'date' => Time.parse(spans[0].content).to_s,
    'subject' => spans[1].content.to_s,
    'uri' => TopUri + spans[1].xpath('a')[0]['href'].to_s
    
  }
  id = id + 1
end

# 保存
#ScraperWiki.sqliteexecute('DELETE FROM JapanNationalPolicyUnit_Scraping')
ScraperWiki.save(['id'], datas)
