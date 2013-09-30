###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'
Process.exit!
# retrieve a page
start_page = 1
end_page = 1
current_page = 1

uri_base = 'http://www.xlr8r.com'
podcast_pages = []

while current_page <= end_page
  starting_url = "#{uri_base}/podcast?page=#{current_page}"
  html = ScraperWiki.scrape(starting_url)

  # use Nokogiri to get all <a> tags
  doc = Nokogiri::HTML(html)
  doc.css('.post .post-cont>a').each do |a|
    podcast_pages << a["href"]
  end

  doc.css('.pager .last').each do |a|
    matches = a["href"].match(/page=(\d+)/)
    if matches and matches[1].to_i != end_page
      end_page = matches[1].to_i
      puts "Updating end page to #{end_page}"
    end
  end

  current_page += 1
end

puts "Podcasts:"
puts podcast_pages.inspect
podcast_pages.each do |page|
  page_url = "#{uri_base}#{page}"
  html = ScraperWiki.scrape(page_url)

  # use Nokogiri to get all <a> tags
  doc = Nokogiri::HTML(html)
  podcast_links = {}
  matches = html.scan(/"(http:\/\/media.xlr8r.com\/files\/podcast\/(m4a|mp3)\/.*)"/)
  puts matches.inspect
  matches.each do |match|
    puts "url=#{match[0]}"
    ScraperWiki.save_sqlite(unique_keys=['type','url'], data={'type' => match[1], 'url' => match[0]})
  end
  if !matches
    ScraperWiki.save_sqlite(unique_keys=['type','url'], data={'type' => 'error', 'url' => page_url})
  end
end###############################################################################
# Basic scraper
###############################################################################

require 'nokogiri'
Process.exit!
# retrieve a page
start_page = 1
end_page = 1
current_page = 1

uri_base = 'http://www.xlr8r.com'
podcast_pages = []

while current_page <= end_page
  starting_url = "#{uri_base}/podcast?page=#{current_page}"
  html = ScraperWiki.scrape(starting_url)

  # use Nokogiri to get all <a> tags
  doc = Nokogiri::HTML(html)
  doc.css('.post .post-cont>a').each do |a|
    podcast_pages << a["href"]
  end

  doc.css('.pager .last').each do |a|
    matches = a["href"].match(/page=(\d+)/)
    if matches and matches[1].to_i != end_page
      end_page = matches[1].to_i
      puts "Updating end page to #{end_page}"
    end
  end

  current_page += 1
end

puts "Podcasts:"
puts podcast_pages.inspect
podcast_pages.each do |page|
  page_url = "#{uri_base}#{page}"
  html = ScraperWiki.scrape(page_url)

  # use Nokogiri to get all <a> tags
  doc = Nokogiri::HTML(html)
  podcast_links = {}
  matches = html.scan(/"(http:\/\/media.xlr8r.com\/files\/podcast\/(m4a|mp3)\/.*)"/)
  puts matches.inspect
  matches.each do |match|
    puts "url=#{match[0]}"
    ScraperWiki.save_sqlite(unique_keys=['type','url'], data={'type' => match[1], 'url' => match[0]})
  end
  if !matches
    ScraperWiki.save_sqlite(unique_keys=['type','url'], data={'type' => 'error', 'url' => page_url})
  end
end