# -*- coding: utf-8 -*-
require 'open-uri'
require "nokogiri"
require 'uri'

url = "http://www.osakabayarea.com/news.html"

html = ScraperWiki.scrape(url).force_encoding("SHIFT_JIS")
doc = Nokogiri::HTML(html.encode("utf-8"),nil)


id = 0;

doc.search('//html/body/table[2]/tr').each do |tr|
    event = tr.search('span[@class="px12"]')
    if event.empty? then
      event = tr.search('td')
    end

    date = event.inner_text.scan(/20[0-9]+.[0-9]+.[0-9]+/).to_s
    date = Time.parse(date)
    if event.search('a').empty? then
      title = event.inner_text
    else
      title = event.search('a').text
      href = event.search('a').attr('href').value
      href = URI::join('http://www.osakabayarea.com/',href)
    end
    data = {
      'id' => id,
      'date'=> date,
      'title' => title,
      'href' => href,
    }
#    puts data
#    puts data.to_json
    ScraperWiki.save_sqlite(unique_keys=['date'], data=data)
    id += 1
end


