require 'nokogiri'

starting_url = 'http://www.bbc.co.uk/news/world-middle-east-12307698'
html = ScraperWiki.scrape(starting_url)

def munge_string(str)
  accents = { 
    ['á','à','â','ä','ã'] => 'a',
    ['Ã','Ä','Â','À','�?'] => 'A',
    ['é','è','ê','ë'] => 'e',
    ['Ë','É','È','Ê'] => 'E',
    ['í','ì','î','ï'] => 'i',
    ['�?','Î','Ì','�?'] => 'I',
    ['ó','ò','ô','ö','õ'] => 'o',
    ['Õ','Ö','Ô','Ò','Ó'] => 'O',
    ['ú','ù','û','ü'] => 'u',
    ['Ú','Û','Ù','Ü'] => 'U',
    ['ç'] => 'c', ['Ç'] => 'C',
    ['ñ'] => 'n', ['Ñ'] => 'N'
  }
  accents.each do |ac,rep|
    ac.each do |s|
      str = str.gsub(s, rep)
    end
  end
  str = str.gsub(/[^a-zA-Z0-9\.,;:\- \'\"\)\(\/\|\&\?\!=<>]/,"")
  str = str.gsub(/[ ]+/," ")
  str = str.gsub(/&amp;/, "&")
  str = str.gsub(/&gt;/, ">")
  str.strip
end

doc = Nokogiri::HTML(html)
doc.search('.lp-wrap div').each do |div|
    time = div.search('strong').inner_html[0..3]
    text = div.search('span').inner_html
    record = {'time' => time, 'text' => munge_string(text)}
    ScraperWiki.save(['time'], record)
end
require 'nokogiri'

starting_url = 'http://www.bbc.co.uk/news/world-middle-east-12307698'
html = ScraperWiki.scrape(starting_url)

def munge_string(str)
  accents = { 
    ['á','à','â','ä','ã'] => 'a',
    ['Ã','Ä','Â','À','�?'] => 'A',
    ['é','è','ê','ë'] => 'e',
    ['Ë','É','È','Ê'] => 'E',
    ['í','ì','î','ï'] => 'i',
    ['�?','Î','Ì','�?'] => 'I',
    ['ó','ò','ô','ö','õ'] => 'o',
    ['Õ','Ö','Ô','Ò','Ó'] => 'O',
    ['ú','ù','û','ü'] => 'u',
    ['Ú','Û','Ù','Ü'] => 'U',
    ['ç'] => 'c', ['Ç'] => 'C',
    ['ñ'] => 'n', ['Ñ'] => 'N'
  }
  accents.each do |ac,rep|
    ac.each do |s|
      str = str.gsub(s, rep)
    end
  end
  str = str.gsub(/[^a-zA-Z0-9\.,;:\- \'\"\)\(\/\|\&\?\!=<>]/,"")
  str = str.gsub(/[ ]+/," ")
  str = str.gsub(/&amp;/, "&")
  str = str.gsub(/&gt;/, ">")
  str.strip
end

doc = Nokogiri::HTML(html)
doc.search('.lp-wrap div').each do |div|
    time = div.search('strong').inner_html[0..3]
    text = div.search('span').inner_html
    record = {'time' => time, 'text' => munge_string(text)}
    ScraperWiki.save(['time'], record)
end
