# -*- coding: shift_jis -*-

require 'nokogiri'

url = 'http://www.mds.gr.jp/~jp3nfp/station/list/jr/chuou.html'
html = ScraperWiki.scrape(url)
doc = Nokogiri::HTML(html)

doc.search("table tr").map do |tr|
  cells = tr.search('td')

  data = {
    'StationName' => cells[1].inner_html.gsub(/<font.*?>/,'').gsub(/<\/font.*?>/, ''),
    'CumilativeDistance' => cells[4].inner_html.gsub(/<font.*?>/,'').gsub(/<\/font.*?>/, ''),
    'BlockDistance' => cells[5].inner_html.gsub(/<font.*?>/,'').gsub(/<\/font.*?>/, '')
  }
  ScraperWiki.save_sqlite(['StationName'], data)
end 