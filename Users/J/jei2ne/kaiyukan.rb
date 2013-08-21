# -*- coding: utf-8 -*-
require "nokogiri"

html = ScraperWiki.scrape("http://www.kaiyukan.com/thv/marketplace/performance/index.html")
doc = Nokogiri::HTML(html)

id = 0;
doc.search('//*[@id="schedulmain"]/ul').each do |ul|
  ul.search('li/table/tr').each do |tr|
    if tr.xpath('th').empty? then
      data = {
        'id' => id,
        'date' => tr.search('table/tr/th').text,
        'performer' => tr.search('table/tr/td').text
      }
    else
      data = {
        'id' => id,
        'date' => tr.xpath('th').text,
        'performer' => tr.xpath('td').text
      }
    end
#    puts data.to_json
    ScraperWiki.save_sqlite(unique_keys=['date'], data=data)
    id += 1;
  end
end


