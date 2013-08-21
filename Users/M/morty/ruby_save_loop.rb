Inf = 1.0 / 0.0
(36000..Inf).each do |i|
  #ScraperWiki.scrape("http://morty.co.uk/?tom=#{i}")
  #Net::HTTP.get_response(URI.parse("http://morty.co.uk/?tom=#{i}"))
  begin
    #http = Net::HTTP.new('morty.co.uk', 80)
    #http.read_timeout = 80
    #http.get("/sleep.php?test=#{i}")
    ScraperWiki.scrape("http://morty.co.uk/sleep.php?tom=#{i}")
  rescue Timeout::Error
    puts "An Error Occured"
  end
end