require 'nokogiri'
html = ScraperWiki::scrape("http://500px.com/market/just_sold")

doc = Nokogiri::HTML(html, nil, "UTF-8")
doc.search("div[@class='photo medium']").each do |photo|
  data = {
    author_name: photo["data-photo-author-name"],
    author_username: photo["data-photo-author-username"],
    photo_id: photo["data-photo-id"],
    photo_name: photo["data-photo-name"],
    src: photo.search('a img')[0]['src'],
    rating: photo.search("div[@class='rating ']")[0].inner_html.to_f,
    timestamp: Time.now
  }

  if (ScraperWiki.select("* from swdata where `photo_id`='#{data[:photo_id]}'").empty? rescue true)
    ScraperWiki.save_sqlite(['photo_id'], data)
  else
    puts "Skipping already saved record " + data[:photo_id]
  end

end
require 'nokogiri'
html = ScraperWiki::scrape("http://500px.com/market/just_sold")

doc = Nokogiri::HTML(html, nil, "UTF-8")
doc.search("div[@class='photo medium']").each do |photo|
  data = {
    author_name: photo["data-photo-author-name"],
    author_username: photo["data-photo-author-username"],
    photo_id: photo["data-photo-id"],
    photo_name: photo["data-photo-name"],
    src: photo.search('a img')[0]['src'],
    rating: photo.search("div[@class='rating ']")[0].inner_html.to_f,
    timestamp: Time.now
  }

  if (ScraperWiki.select("* from swdata where `photo_id`='#{data[:photo_id]}'").empty? rescue true)
    ScraperWiki.save_sqlite(['photo_id'], data)
  else
    puts "Skipping already saved record " + data[:photo_id]
  end

end
