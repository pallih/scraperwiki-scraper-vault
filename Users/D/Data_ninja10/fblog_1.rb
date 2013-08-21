# Blank Ruby
puts "Hello, coding in the cloud!"

(2010..2020).each { |y| 
  (1..12).each { |m|
    url = "http://ejercitogeek.net/?mon="
    url += y.to_s
    if m < 10
      url += "0"
    end
    url += m.to_s
    html = ScraperWiki.scrape(url)
    counter=0
    count_posts = html.scan("<li>").size 
    count_ehemalige = html.scan("ehemalige").size 
    count_terror = html.scan("terror").size 

    data_count = { 'year' => y, 'month' => m, 'count_posts' => count_posts, 'count_ehemalige' => count_ehemalige, 'count_terror' => count_terror}
    ScraperWiki.save_sqlite(unique_keys=['year', 'month'], data=data_count) 

    puts y.to_s + " "+ m.to_s
  }
}
