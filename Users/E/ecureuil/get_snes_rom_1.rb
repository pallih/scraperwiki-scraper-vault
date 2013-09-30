require 'nokogiri'

MAIN_URL = "http://www.rom-world.com"

def save_games(letter = "0-9")
 
  html = ScraperWiki.scrape("#{MAIN_URL}/dl.php?name=Nintendo&letter=#{letter}")

  parser = Nokogiri::HTML(html)

  parser.search("table.games a").each do |game|
    download_page  = ScraperWiki.scrape(MAIN_URL + game["href"])
    download_link = Nokogiri::HTML(download_page)

    record = {"name" => game.text}

    (download_link/"table table table a").each do |links|
      record["link"] = links["href"] if links["href"] =~ /\.zip/
    end
  
    ScraperWiki.save(["link"], record)
  end
end

save_games()
('A'..'Z').each do |l|
   save_games(l)
endrequire 'nokogiri'

MAIN_URL = "http://www.rom-world.com"

def save_games(letter = "0-9")
 
  html = ScraperWiki.scrape("#{MAIN_URL}/dl.php?name=Nintendo&letter=#{letter}")

  parser = Nokogiri::HTML(html)

  parser.search("table.games a").each do |game|
    download_page  = ScraperWiki.scrape(MAIN_URL + game["href"])
    download_link = Nokogiri::HTML(download_page)

    record = {"name" => game.text}

    (download_link/"table table table a").each do |links|
      record["link"] = links["href"] if links["href"] =~ /\.zip/
    end
  
    ScraperWiki.save(["link"], record)
  end
end

save_games()
('A'..'Z').each do |l|
   save_games(l)
end