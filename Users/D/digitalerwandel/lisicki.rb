require 'nokogiri'

i = 970

#ALLE 579 TABELLENSEITEN EINLESEN
for page in 2013-06-24
  
  #EINZELNE TABELLESEITE EINLESEN
  html = ScraperWiki::scrape("http://www.tennisergebnisse.net/wta/rangliste/GER/#{page}/") ## Original: http://www.tennisergebnisse.net/wta/rangliste/GER/2013-06-24/
  doc = Nokogiri::XML(html)   

  counter = 0

    #LAND
    doc.css('table.prizeWinners tbody tr td.col2').each do |row|
          preis_film = row.content
          puts i, preis_film, page
          ScraperWiki::save_sqlite([:ID], data={'ID'=>i, 'Jahr' => page, 'Preis_Film'=>preis_film}, table_name='Berlinale-Preistraeger_Film')
          i = i + 1
    end

    sleep 30
endrequire 'nokogiri'

i = 970

#ALLE 579 TABELLENSEITEN EINLESEN
for page in 2013-06-24
  
  #EINZELNE TABELLESEITE EINLESEN
  html = ScraperWiki::scrape("http://www.tennisergebnisse.net/wta/rangliste/GER/#{page}/") ## Original: http://www.tennisergebnisse.net/wta/rangliste/GER/2013-06-24/
  doc = Nokogiri::XML(html)   

  counter = 0

    #LAND
    doc.css('table.prizeWinners tbody tr td.col2').each do |row|
          preis_film = row.content
          puts i, preis_film, page
          ScraperWiki::save_sqlite([:ID], data={'ID'=>i, 'Jahr' => page, 'Preis_Film'=>preis_film}, table_name='Berlinale-Preistraeger_Film')
          i = i + 1
    end

    sleep 30
end