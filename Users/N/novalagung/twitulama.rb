require 'nokogiri'
require 'open-uri'

page = 0
loop = true
i = 1

while true and loop
  data = Nokogiri::HTML(open("http://twitulama.com/page/#{page}")).css(".posts .post.quote")

  loop = false if data.length < 1 || page > 10

  data.each do |v,e|
    source = v.css(".source.hasMarkup")
    twitter = Array.new
    twitter[0] = v.attribute("data-id")
    twitter[1] = v.css(".echo.hasMarkup.fS").inner_html.gsub(/<\/?[^>]*>/, "").strip
    twitter[2] = source.search("a").inner_html.gsub(/@/, "").gsub(/<\/?[^>]*>/, "").strip
    twitter[3] = source.to_s.gsub(/#{source.search("a")}/, "").gsub(/<\/?[^>]*>/, "").gsub(/@/, "").gsub(/-/, "").strip
    puts twitter

    ScraperWiki::save_sqlite(unique_keys = [:i], data = {:i => i, :id => twitter[0], :tweet => twitter[1], :twitter => twitter[2], :name => twitter[3]}) 
    i += 1
  end

  page += 1
endrequire 'nokogiri'
require 'open-uri'

page = 0
loop = true
i = 1

while true and loop
  data = Nokogiri::HTML(open("http://twitulama.com/page/#{page}")).css(".posts .post.quote")

  loop = false if data.length < 1 || page > 10

  data.each do |v,e|
    source = v.css(".source.hasMarkup")
    twitter = Array.new
    twitter[0] = v.attribute("data-id")
    twitter[1] = v.css(".echo.hasMarkup.fS").inner_html.gsub(/<\/?[^>]*>/, "").strip
    twitter[2] = source.search("a").inner_html.gsub(/@/, "").gsub(/<\/?[^>]*>/, "").strip
    twitter[3] = source.to_s.gsub(/#{source.search("a")}/, "").gsub(/<\/?[^>]*>/, "").gsub(/@/, "").gsub(/-/, "").strip
    puts twitter

    ScraperWiki::save_sqlite(unique_keys = [:i], data = {:i => i, :id => twitter[0], :tweet => twitter[1], :twitter => twitter[2], :name => twitter[3]}) 
    i += 1
  end

  page += 1
end