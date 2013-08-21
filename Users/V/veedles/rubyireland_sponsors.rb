require 'scraperwiki'
require 'active_support'
require 'nokogiri'

html = ScraperWiki::scrape("http://www.meetup.com/rubyireland/")
doc = Nokogiri::HTML(html)

sponsor_list = doc.search("div.D_sponsors div.D_boxsection div.sponsorSlot").map do |v|
  {
    name: v.search('a').map(&:inner_text).reject{|item| item == ''}.first,
    url: v.at('a').attribute_nodes.map(&:value).reject{|item| item == '_blank'}.first,
    blurb: v.at('p').inner_text,
    img_url: v.at('a img').attribute_nodes[0].value
  }
end

data = {:sponsor_list => sponsor_list.to_json}

ScraperWiki::save_sqlite([:sponsor_list], data)
