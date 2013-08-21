# encoding: utf-8

require 'nokogiri'
require 'open-uri'

BASE_URL = "http://www.funkdascomunidades.net/download-de-musicas.php"

def parser(url)
  html = open(url, {"User-Agent" => "Eh noiz Q ta nu Ruby"}).read
  Nokogiri::HTML(html)
end

def download_funk(category)

  target = "#{BASE_URL}?cat=#{category}"
  
  music_index_parser = parser(target)
  
  music_index_parser.search(".download-funk").each do |parser_musica|
    begin
      music_show_link = parser_musica.search("a")[0].attr("href")
      music_show_parser = parser("#{BASE_URL}#{music_show_link}")
    
      music_info = music_show_parser.search("#interna_a")
      
      name = music_info.search("h2").text()
      link = music_info.search(".texto a").attr("href")
      download = parser_musica.search(".contador").text()
      date = parser_musica.search(".data").text()
    
      ScraperWiki.save(["name"], {name: name, link: link, download: download.to_i, date: date, category: category})
    rescue
      next
    end
  end
end

download_funk("funk--p")
download_funk("funk-atual")
download_funk("dj-luizinho")