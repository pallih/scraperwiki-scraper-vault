# Blank Ruby
puts "Starting Scrape of Committee Members"
html = ScraperWiki.scrape("http://www.surreylawsociety.org.uk/about/committee.php")

require 'nokogiri'           

docCat = Nokogiri::HTML(html)
data = Hash.new

members = docCat.css('.people li').each { |member|
  data['member_name'] = member.search('.details h2').inner_html
  data['member_position'] = member.search('.details p.job').inner_html
  data['member_email'] = member.search('.details p.email a').attr('href').to_s.gsub('mailto:', '')
  data['member_phone'] = member.search('.details p.tel').inner_html
  data['member_bio'] = member.search('p').last().inner_html
  data['member_img'] = member.search('.thumb img').attr('src')

  ScraperWiki.save_sqlite(unique_keys=['member_name'], data=data)
}

# Blank Ruby
puts "Starting Scrape of Committee Members"
html = ScraperWiki.scrape("http://www.surreylawsociety.org.uk/about/committee.php")

require 'nokogiri'           

docCat = Nokogiri::HTML(html)
data = Hash.new

members = docCat.css('.people li').each { |member|
  data['member_name'] = member.search('.details h2').inner_html
  data['member_position'] = member.search('.details p.job').inner_html
  data['member_email'] = member.search('.details p.email a').attr('href').to_s.gsub('mailto:', '')
  data['member_phone'] = member.search('.details p.tel').inner_html
  data['member_bio'] = member.search('p').last().inner_html
  data['member_img'] = member.search('.thumb img').attr('src')

  ScraperWiki.save_sqlite(unique_keys=['member_name'], data=data)
}

