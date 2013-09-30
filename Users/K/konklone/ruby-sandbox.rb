require 'nokogiri'

Nokogiri::HTML(ScraperWiki.scrape("http://mill-industries.com")).search("//article").each do |article|
  ScraperWiki.save_sqlite(['slug'], {
    :body => (article / :p).map {|p| p.text}.join("\n\n"),
    :title => article.css("header h1 a").first.text,
    :slug => article.css("header h1 a").first['href'].sub(/^\/post\//, '')
  })
endrequire 'nokogiri'

Nokogiri::HTML(ScraperWiki.scrape("http://mill-industries.com")).search("//article").each do |article|
  ScraperWiki.save_sqlite(['slug'], {
    :body => (article / :p).map {|p| p.text}.join("\n\n"),
    :title => article.css("header h1 a").first.text,
    :slug => article.css("header h1 a").first['href'].sub(/^\/post\//, '')
  })
end