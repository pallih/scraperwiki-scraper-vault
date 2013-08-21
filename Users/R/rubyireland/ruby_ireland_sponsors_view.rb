sourcescraper = 'ruby_ireland_sponsors_scraper'
ScraperWiki::attach(sourcescraper)

data = ScraperWiki::select( "* from ruby_ireland_sponsors_scraper.swdata")

puts %^
<style TYPE="text/css">

body {
    color: #333333;
    font-family: "Lora",Georgia,"Times New Roman",Times,serif;
    font-size: 17px;
    line-height: 26px;
}

ul {
    list-style: none;
    padding: none;
}
</style>
^

puts "<br />"
puts "<br />"
puts "<br />"

puts "<ul>"

JSON::parse(data.first['sponsor_list']).each do |sponsor|
  puts "<li>"
  puts %^<a href="#{sponsor['url']}" target="_blank"><img src="#{sponsor['img_url']}"></a>^
  puts "<p>"
  puts %^<a href="#{sponsor['url']}" target="_blank">#{sponsor['name']}</a>^
  puts "#{sponsor['blurb']}"
  puts "</p>"
  puts "</li>"

  #All available data
  #puts "#{sponsor['name']}"
  #puts "#{sponsor['url']}"
  #puts "#{sponsor['blurb']}"
  #puts "#{sponsor['img_url']}"
end

puts "</ul>"
