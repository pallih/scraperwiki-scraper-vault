require 'nokogiri'           
require 'open-uri'

cantons = [
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Aargau",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Appenzell_Ausserrhoden",
"http://de.wikipedia.org/wiki/Bezirke_des_Kantons_Appenzell_Innerrhoden",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Basel-Landschaft",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Basel-Stadt",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Bern",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Freiburg",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Genf",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Glarus",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Graub%C3%BCnden",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Jura",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Luzern",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Neuenburg",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Nidwalden",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Obwalden",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Schaffhausen",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Schwyz",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Solothurn",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_St._Gallen",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Tessin",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Thurgau",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Uri",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Waadt",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Wallis",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Zug",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Z%C3%BCrich"
]

cantons.each do |canton|
  doc = Nokogiri::HTML( open( canton ) )

  doc.xpath('//div[@id="mw-content-text"]//tr').each do |tr|
    tds = tr.css('td')

    next unless tds.size >= 3

    begin
      data = {
        :wappen => tds[0].css('a img').attribute('src').to_s,
        :link => tds[1].css('a').attribute('href').to_s.gsub('/wiki/',''),
        :name => tds[1].content
      }
      ScraperWiki.save_sqlite(unique_keys=[ :link ], data )
    rescue
      puts "problem in #{ canton }"
      puts tds.inspect
    end
  end
endrequire 'nokogiri'           
require 'open-uri'

cantons = [
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Aargau",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Appenzell_Ausserrhoden",
"http://de.wikipedia.org/wiki/Bezirke_des_Kantons_Appenzell_Innerrhoden",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Basel-Landschaft",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Basel-Stadt",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Bern",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Freiburg",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Genf",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Glarus",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Graub%C3%BCnden",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Jura",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Luzern",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Neuenburg",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Nidwalden",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Obwalden",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Schaffhausen",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Schwyz",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Solothurn",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_St._Gallen",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Tessin",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Thurgau",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Uri",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Waadt",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Wallis",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Zug",
"http://de.wikipedia.org/wiki/Gemeinden_des_Kantons_Z%C3%BCrich"
]

cantons.each do |canton|
  doc = Nokogiri::HTML( open( canton ) )

  doc.xpath('//div[@id="mw-content-text"]//tr').each do |tr|
    tds = tr.css('td')

    next unless tds.size >= 3

    begin
      data = {
        :wappen => tds[0].css('a img').attribute('src').to_s,
        :link => tds[1].css('a').attribute('href').to_s.gsub('/wiki/',''),
        :name => tds[1].content
      }
      ScraperWiki.save_sqlite(unique_keys=[ :link ], data )
    rescue
      puts "problem in #{ canton }"
      puts tds.inspect
    end
  end
end