require 'nokogiri'

MAIN_URL = "http://www.rom-world.com"

def parser(url)
  page = ScraperWiki.scrape(MAIN_URL + url)
  Nokogiri::HTML(page)
end

def save_games(ref)
  game_page = parser("/dl.php?name=Nintendo&letter=#{ref}")

  game_page.search("table.games a").each do |rom|
    record = {"name" => rom.text} 
    download_page = parser(rom['href'])

    (download_page/"table table table a").each do |links|
      record["link"] = links["href"] if links["href"] =~ /\.zip/
    end
  
    ScraperWiki.save(["link"], record)
  end
end

save_games("0-9")

('A'..'Z').each do |letter|
   save_games(letter)
endrequire 'nokogiri'

MAIN_URL = "http://www.rom-world.com"

def parser(url)
  page = ScraperWiki.scrape(MAIN_URL + url)
  Nokogiri::HTML(page)
end

def save_games(ref)
  game_page = parser("/dl.php?name=Nintendo&letter=#{ref}")

  game_page.search("table.games a").each do |rom|
    record = {"name" => rom.text} 
    download_page = parser(rom['href'])

    (download_page/"table table table a").each do |links|
      record["link"] = links["href"] if links["href"] =~ /\.zip/
    end
  
    ScraperWiki.save(["link"], record)
  end
end

save_games("0-9")

('A'..'Z').each do |letter|
   save_games(letter)
end