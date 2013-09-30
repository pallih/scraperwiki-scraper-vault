# coding: utf-8
require 'nokogiri'           
html = ScraperWiki::scrape("http://connections.sg/")

# ignore hi unicode characters that are on the page (and break the nokogiri version on ScraperWiki)
html_clean = html.unpack("U*").map{|c| c < 255 ? c.chr : ' ' }.join


doc = Nokogiri::HTML(html_clean)

block_views = doc.css('section.block-views')

block_views.each do |block_view|
  block_title = if block_h = block_view.css('h3').first
    block_h.text
  else
    'Other'
  end

  items = block_view.css('.item-list li')
  items.each do |item|
    item_title = if item_h = item.css('h5').first
      item_h.text
    end
    item_url = if link = item.css('a').first
      item_title = link.text unless item_title
      link[:href]
    end
    data = {
      category: block_title,
      title: item_title,
      url: item_url
    }
    #puts data.to_json
    ScraperWiki::save_sqlite(['url'], data)
  end
end# coding: utf-8
require 'nokogiri'           
html = ScraperWiki::scrape("http://connections.sg/")

# ignore hi unicode characters that are on the page (and break the nokogiri version on ScraperWiki)
html_clean = html.unpack("U*").map{|c| c < 255 ? c.chr : ' ' }.join


doc = Nokogiri::HTML(html_clean)

block_views = doc.css('section.block-views')

block_views.each do |block_view|
  block_title = if block_h = block_view.css('h3').first
    block_h.text
  else
    'Other'
  end

  items = block_view.css('.item-list li')
  items.each do |item|
    item_title = if item_h = item.css('h5').first
      item_h.text
    end
    item_url = if link = item.css('a').first
      item_title = link.text unless item_title
      link[:href]
    end
    data = {
      category: block_title,
      title: item_title,
      url: item_url
    }
    #puts data.to_json
    ScraperWiki::save_sqlite(['url'], data)
  end
end