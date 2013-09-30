# AKB48 sosenkyo 3
require 'nokogiri'
require 'open-uri'
$KCODE='u'
yen_for_cd = 1500

doc = Nokogiri::HTML(open('http://www.yomiuri.co.jp/entertainment/news2/20110610-OYT8T00780.htm'),nil,'SHIFT_JIS')
puts doc.content
akbs = doc.css("div.article-def p").map do |akb|
  akb = akb.inner_text.scan(/(\d+)[　\s](.+ ?.+) ([\d,]+)/).first
  record = {
    'order' => akb[0].to_i,
    'name' => akb[1].to_s,
    'money' => akb[2].delete(',').to_i * yen_for_cd,
    'votes' => akb[2].delete(',').to_i
  }
  p record
  ScraperWiki.save(['name'], record)
end# AKB48 sosenkyo 3
require 'nokogiri'
require 'open-uri'
$KCODE='u'
yen_for_cd = 1500

doc = Nokogiri::HTML(open('http://www.yomiuri.co.jp/entertainment/news2/20110610-OYT8T00780.htm'),nil,'SHIFT_JIS')
puts doc.content
akbs = doc.css("div.article-def p").map do |akb|
  akb = akb.inner_text.scan(/(\d+)[　\s](.+ ?.+) ([\d,]+)/).first
  record = {
    'order' => akb[0].to_i,
    'name' => akb[1].to_s,
    'money' => akb[2].delete(',').to_i * yen_for_cd,
    'votes' => akb[2].delete(',').to_i
  }
  p record
  ScraperWiki.save(['name'], record)
end