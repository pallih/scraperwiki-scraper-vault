require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'pp'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'

def download_credits(link, contatore_aggiornato)

url = link

doc = Nokogiri.HTML(open(url))
#puts doc

rows = doc.search('tr') #dò a rows il contenuto di ogni riga della tabella dei credits dell'album che sto analizzando
#puts rows
artist_url = doc.search('#wrapper .album-artist')[0] #prende la riga in alto a sinistra dove c'è il nome e il link dell'artista
#puts artist_url

rows.each do |row| #start of the iteration on the rows  
  link = row.search('a')[0]
  #puts link

  credit = {}
  
  credit[:id] = contatore_aggiornato
  
  #credit[:lfm_a_name] = artist_url.inner_text #prende il nome dell'artista autore dell'album
  
  credit[:am_url] = artist_url.search('a').map { |link| link[:href]} #prende il link dell'artista autore dell'album
  
  credit[:person_name] = link.inner_text #prende il nome del collab
  
  credit[:album_url] = url #prende il link della pagina da cui si scaricano i dati e a cui va tolto successivamente la stringa /credits
  
  credit[:person_url] = link[:href] #prende l'URL del collab
  
  credit[:credit] = row.search('.name-credit').inner_text.strip #prende il ruolo che il collab ha avuto nell'album analizzato
  

contatore_aggiornato = contatore_aggiornato + 1

ScraperWiki::save_sqlite([:id], credit, table_name="ALL_credits_info", verbose=0)
#ScraperWiki.save([:id], credit)

end #ends the iteration on the rows

contatore_aggiornato = contatore_aggiornato + 1

return contatore_aggiornato

#cont = contatore_aggiornato

end #ends method def


ScraperWiki::attach("all_artists_albums_url_e_info_definitivo_step_1_1_", "step1")#prende le informazioni dallo scraper step 1 con solo i link degli
                                                                                  #album dell'artista(bisogna usare l'url dello scraper!!) e inoltre
                                                                                  #cambia il nome dello scraper in uno dato da me che in questo caso è
                                                                                  #'step1'

#pp ScraperWiki::table_info("step1.swdata")
cont=0

data = ScraperWiki::select(              #prende i dati dalla tabella 'data' dello scraper step 1
    "* from step1.ONLY_albums_URL
    order by album_url desc limit 150"    #il limite di righe che può prendere in questo caso è 50
)
data.each do |slot|                      #itera negli elementi dell'hash di dati provenienti dallo step1
  #puts slot
  
  slot.each do |x|                       #itera sugli url singoli dello step 1
    link_allmusic = x[1]+"/credits"
                                         #cambia l'url dell'album aggiungendo "/credits" per accedere alla pagina dei credits di ogni album
    #puts link
    if cont==0
     cont = download_credits(link_allmusic, cont)      #invocazione del metodo 'download_credits' con passaggio di volta in volta del link da cui scaricare i #credits
      
    else 
      cont = download_credits(link_allmusic, cont)

    end                                  #fine dell'if-else 
  end                                    #fine del primo ciclo di iterazione sugli slot
end                                      #fine del secondo ciclo di iterazione sui link
require 'nokogiri'
require 'open-uri'
require 'date'
require 'yaml'
require 'json'
require 'pp'
require 'uri'
require 'net/http'
require 'scraperwiki/datastore'
require 'httpclient'
require 'scraperwiki/scraper_require'

def download_credits(link, contatore_aggiornato)

url = link

doc = Nokogiri.HTML(open(url))
#puts doc

rows = doc.search('tr') #dò a rows il contenuto di ogni riga della tabella dei credits dell'album che sto analizzando
#puts rows
artist_url = doc.search('#wrapper .album-artist')[0] #prende la riga in alto a sinistra dove c'è il nome e il link dell'artista
#puts artist_url

rows.each do |row| #start of the iteration on the rows  
  link = row.search('a')[0]
  #puts link

  credit = {}
  
  credit[:id] = contatore_aggiornato
  
  #credit[:lfm_a_name] = artist_url.inner_text #prende il nome dell'artista autore dell'album
  
  credit[:am_url] = artist_url.search('a').map { |link| link[:href]} #prende il link dell'artista autore dell'album
  
  credit[:person_name] = link.inner_text #prende il nome del collab
  
  credit[:album_url] = url #prende il link della pagina da cui si scaricano i dati e a cui va tolto successivamente la stringa /credits
  
  credit[:person_url] = link[:href] #prende l'URL del collab
  
  credit[:credit] = row.search('.name-credit').inner_text.strip #prende il ruolo che il collab ha avuto nell'album analizzato
  

contatore_aggiornato = contatore_aggiornato + 1

ScraperWiki::save_sqlite([:id], credit, table_name="ALL_credits_info", verbose=0)
#ScraperWiki.save([:id], credit)

end #ends the iteration on the rows

contatore_aggiornato = contatore_aggiornato + 1

return contatore_aggiornato

#cont = contatore_aggiornato

end #ends method def


ScraperWiki::attach("all_artists_albums_url_e_info_definitivo_step_1_1_", "step1")#prende le informazioni dallo scraper step 1 con solo i link degli
                                                                                  #album dell'artista(bisogna usare l'url dello scraper!!) e inoltre
                                                                                  #cambia il nome dello scraper in uno dato da me che in questo caso è
                                                                                  #'step1'

#pp ScraperWiki::table_info("step1.swdata")
cont=0

data = ScraperWiki::select(              #prende i dati dalla tabella 'data' dello scraper step 1
    "* from step1.ONLY_albums_URL
    order by album_url desc limit 150"    #il limite di righe che può prendere in questo caso è 50
)
data.each do |slot|                      #itera negli elementi dell'hash di dati provenienti dallo step1
  #puts slot
  
  slot.each do |x|                       #itera sugli url singoli dello step 1
    link_allmusic = x[1]+"/credits"
                                         #cambia l'url dell'album aggiungendo "/credits" per accedere alla pagina dei credits di ogni album
    #puts link
    if cont==0
     cont = download_credits(link_allmusic, cont)      #invocazione del metodo 'download_credits' con passaggio di volta in volta del link da cui scaricare i #credits
      
    else 
      cont = download_credits(link_allmusic, cont)

    end                                  #fine dell'if-else 
  end                                    #fine del primo ciclo di iterazione sugli slot
end                                      #fine del secondo ciclo di iterazione sui link
