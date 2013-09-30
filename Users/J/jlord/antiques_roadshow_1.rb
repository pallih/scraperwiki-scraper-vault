#encoding: utf-8
require 'nokogiri'
require 'open-uri'

u = "http://www.pbs.org/cgi-registry/wgbh/roadshow/archive_search.cgi?q=&category=&appraiser=&city=&episode=&season=&value_min=&value_max=&x=&y=13"

doc = Nokogiri::HTML(open(u))

doc.css('.result_item').each do |item|
  data = {
    'Link' => "http://www.pbs.org" + item.search("a").first.attribute("href").to_s
  }
  data["Title"] = item.css(".result_title").first.text.encode("US-ASCII", undef: :replace, invalid: :replace)

  for a in item.search("div[@class=summary] span[@class=label]")
    k = a.xpath("text()").to_s.strip.gsub(/:/, '')
    v = a.xpath("following-sibling::text()[1]")
    if v.to_s != " "
      data[k] = v
    end
  end

  ScraperWiki.save_sqlite(unique_keys=['Link', 'Title', 'Episode', 'Appraiser', 'Value'], data=data) 
end
#encoding: utf-8
require 'nokogiri'
require 'open-uri'

u = "http://www.pbs.org/cgi-registry/wgbh/roadshow/archive_search.cgi?q=&category=&appraiser=&city=&episode=&season=&value_min=&value_max=&x=&y=13"

doc = Nokogiri::HTML(open(u))

doc.css('.result_item').each do |item|
  data = {
    'Link' => "http://www.pbs.org" + item.search("a").first.attribute("href").to_s
  }
  data["Title"] = item.css(".result_title").first.text.encode("US-ASCII", undef: :replace, invalid: :replace)

  for a in item.search("div[@class=summary] span[@class=label]")
    k = a.xpath("text()").to_s.strip.gsub(/:/, '')
    v = a.xpath("following-sibling::text()[1]")
    if v.to_s != " "
      data[k] = v
    end
  end

  ScraperWiki.save_sqlite(unique_keys=['Link', 'Title', 'Episode', 'Appraiser', 'Value'], data=data) 
end
