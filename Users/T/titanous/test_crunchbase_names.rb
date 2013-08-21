require 'nokogiri'
require 'json'
require 'cgi'
require 'active_support/core_ext/hash'

RAPLEAF_KEY = '9295267031eafd1469e91a03f906904f'

(1..155).each do |n|
  html = ScraperWiki::scrape("http://www.crunchbase.com/search/advanced/people/1277391?page=#{n}")
  doc = Nokogiri::HTML(html)
  records = doc.search("div.search_result_name a").map do |a|
    data = { name: a.inner_html, link: a['href'] }
    if data[:name].strip != ''
      name = data[:name].split(' ').first
      name_data = JSON.parse ScraperWiki::scrape("http://api.rapleaf.com/v4/util/name_to_gender/#{name}?api_key=#{RAPLEAF_KEY}")
      data.merge(name_data['answer']).except("input")
    end
  end.compact
  puts records
  ScraperWiki::save_sqlite(['link'], records)
end
